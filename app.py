from database import conn
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from database import decoder


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


@app.route('/get-problem-by-id' , methods=['GET'])
def getProblemById():
    id = int(request.args.get('id'))
    problems = db.problems
    problem = problems.find_one({'id':id})
    
    # return jsonify(problem)
    return problem



if __name__ == '__main__':
    app.run(debug=True)
