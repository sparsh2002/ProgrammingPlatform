from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException
import os
from dotenv import load_dotenv
from database.conn import client as dbclient
load_dotenv()
accessToken = os.getenv('SPHERE_ENGINE_ACCESS_TOKEN')
endpoint = os.getenv('SPHERE_ENGINE_ENDPOINT')

url = f'https://{endpoint}/api/v4/problems?access_token={accessToken}'

client = ProblemsClientV4(accessToken, endpoint)

db = dbclient['cometlabs']

def creatProblem(data):
    # create a problem in sphere environment
    response = None

    try:
        response = client.problems.create(name = data['name'], body = data['body'] ,masterjudge_id =  int(data['masterjudgeId']))
    # response['id'] stores the ID of the created problem
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
            return 'Invalid access token'
        elif e.code == 400:
            print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
            return 'Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e)
    
    # if successfull then firstly get the problem
    problemId = int(response['id'])
    try:
        response = client.problems.get(problemId)
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
        elif e.code == 403:
            print('Access to the problem is forbidden')
        elif e.code == 404:
            print('Problem does not exist')

    # if retrieved the data , then post it into mongodb
    problems = db.problems

    if problems.find_one({'id' : problemId}) :
        return 'Problem with this Id exists'
    
    problems.insert_one(response)
    
    return 'Problem Created Successfully'
    


def updateProblem(data, problemId):
    # create a problem in sphere environment
    response = None

    try:
        response = client.problems.update( problemId ,name = data['name'], body = data['body'] ,masterjudge_id =  int(data['masterjudgeId']))
    # response['id'] stores the ID of the updated problem
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
            return 'Invalid access token'
        elif e.code == 403:
            print('Access to the problem is forbidden')
            return 'Access to the problem is forbidden'
        elif e.code == 404:
            print('Problem does not exist')
            return 'Problem does not exist'
        elif e.code == 400:
            print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
            return 'Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e)
    
    # if successfull then firstly get the problem
    
    try:
        response = client.problems.get(problemId)
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
        elif e.code == 403:
            print('Access to the problem is forbidden')
        elif e.code == 404:
            print('Problem does not exist')

    # if retrieved the data , then put it into mongodb
    problems = db.problems

    query = {"id":problemId}
    # print(response)
    value = {"$set" : response}
    if  problems.find_one(problemId):
        print('Found')
    problems.update_one(query ,value)
    
    return 'Problem Updated Successfully'


def deleteProblem(problemId):
    response = None
    try:
        response = client.problems.delete(problemId)
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
            return 'Invalid access token'
        elif e.code == 403:
            print('Access to the problem is forbidden')
            return 'Access to the problem is forbidden'
        elif e.code == 404:
            print('Problem does not exist')
            return 'Problem does not exist'
        elif e.code == 400:
            print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
            return 'Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e)
    
    

    # delete from mongodb
    problems = db.problems

    query = {"id":problemId}
   
    problems.delete_one(query)
    
    return 'Deleted Problem Successfully'