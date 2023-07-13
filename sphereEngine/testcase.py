from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

import os
from dotenv import load_dotenv
from database.conn import client as dbclient
load_dotenv()
accessToken = os.getenv('SPHERE_ENGINE_ACCESS_TOKEN')
endpoint = os.getenv('SPHERE_ENGINE_ENDPOINT')

client = ProblemsClientV4(accessToken, endpoint)

db = dbclient['cometlabs']

def createTestCase(problemId , data):
    try:
        response = client.problems.createTestcase(problemId, data['input'], 
                                                  data['output'],  int(data['time_limit']), 
                                                   int(data['judge_id']))
    # response['number'] stores the number of created testcase
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
            return 'Invalid access token'
        elif e.code == 403:
            print('Access to the problem is forbidden')
            return 'Access to the problem is forbidden'
        elif e.code == 404:
            print('Problem does not exist')    
            return 'Proble does not exist'
        elif e.code == 400:
            print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
            return 'Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e)

    num_cases = response['number']

    testcases = db.testcases

    try:
        response = client.problems.allTestcases(problemId)
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
            return 'Invalid access token'
        elif e.code == 403:
            print('Access to the problem is forbidden')
            return 'Access to the problem is forbidden'
        elif e.code == 404:
            print('Problem does not exist')
            return 'the problem does not exist'
    response['problemId'] = problemId
    if testcases.find_one({"id":problemId}):
        testcases.update_one({"id":problemId},{"$set":response})
    else:
        testcases.insert_one(response)


    return f'{num_cases} test cases created successfully for the problem id:{problemId}'


def getAllTestCases():
    return 'Done'


def getTestCase():
    return 'Done'

def updateTestCase():
    return 'Done'