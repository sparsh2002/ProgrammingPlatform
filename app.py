from database import conn
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from database import decoder
from sphereEngine.problems import creatProblem , updateProblem , deleteProblem
from sphereEngine.testcase import createTestCase, getAllTestCases , getTestCase , updateTestCase
load_dotenv()
db = conn.client['cometlabs']
app = Flask(__name__)
app.json_encoder = decoder.MongoJSONEncoder


app.config['SECRET_KEY'] = os.getenv('MY_SECRET')
@app.before_first_request
def create_collections():
    users = db.users
    users.create_index('username', unique=True)
    users.create_index('email', unique=True)

@app.route('/', methods=['GET'])
def home():
    print('Welcome')
    return 'Welcome to this server'

@app.route('/signup', methods=['POST'])
def signup():
    print("Signup Attempted")
    users = db.users
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    role =request.json['role']

    # Check if username or email already exists
    if users.find_one({'$or': [{'username': username}, {'email': email}]}):
        return jsonify({'error': 'Username or email already exists'})

    # Hash the password
    hashed_password = generate_password_hash(password, method='sha256')

    # Create a new user document
    user = {'username': username, 'email': email, 'password': hashed_password , 'role':role}
    users.insert_one(user)

    return jsonify({'message': 'User created successfully'})



@app.route('/login', methods=['POST'])
def login():
    print('login Attempted')
    users = db.users
    username = request.json['username']
    password = request.json['password']
    role = request.json['role']
    # print(username , password, role)
    # Find the user by username
    user = users.find_one({'username': username})
    # print(user)

    # # Check if the user exists and verify the password
    if user and check_password_hash(user['password'], password):
        # Generate JWT token
        token = jwt.encode(
            {
                'username': user['username'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({'token': token})

    return jsonify({'error': 'Invalid username or password'})
    return 'Done'

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Missing token'})

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = decoded['username']
        return jsonify({'message': f'Hello, {username}! This is a protected route.'})

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'})

    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'})


@app.route('/problems' , methods=['GET' , 'POST' , 'PUT' , 'DELETE'])
def Problems():
    problems = db.problems
    if request.method == 'GET':
        if request.args.get('id') is not None:
            id = int(request.args.get('id'))
            problem = problems.find_one({'id':id})
            
            # return jsonify(problem)
            return problem
        else:
            projection = {"_id": 1, "name": 1}

            documents = list(problems.find({}, projection))

            return jsonify(documents)

    elif request.method == 'POST':
        # print(request.json)
        res = creatProblem(request.json)
        return res
        # return 'Done'
    
    elif request.method == 'PUT':
        problemId = int(request.args.get('id'))
        res = updateProblem(request.json , problemId)
        return res
    
    elif request.method == 'DELETE':
        problemId = int(request.args.get('id'))
        res = deleteProblem(problemId)
        return res
    else:

        return 'Method Not Defined'

@app.route('/problems/testcases' , methods=['GET' , 'POST' , 'PUT' ])
def testcases():
    if request.method == 'GET':
        id = request.args.get('id')
        number = request.args.get('number')
        if id is not None and number is not None:
            res = getTestCase(int(id) , int(number))
            return res
        else:
            res = getAllTestCases(int(id))
            return res
    elif request.method == 'POST':
        id = request.args.get('id')
        res = createTestCase(int(id) , request.json)
        return res
    
    elif request.method == 'PUT':
        id = request.args.get('id')
        number = request.args.get('number')
        res = updateTestCase(int(id)  , int(number), request.json)
        return res
    
    
    else:
        return 'Method Not Defined'

if __name__ == '__main__':
    app.run(debug=True)
