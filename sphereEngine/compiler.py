from sphere_engine import ProblemsClientV4
from sphere_engine.exceptions import SphereEngineException

import os
from dotenv import load_dotenv
from database.conn import client as dbclient
load_dotenv()
# accessToken = os.getenv('SPHERE_ENGINE_COMPILER_ACCESS_TOKEN')
accessToken = os.getenv('SPHERE_ENGINE_ACCESS_TOKEN')
endpoint = os.getenv('SPHERE_ENGINE_ENDPOINT')

client = ProblemsClientV4(accessToken, endpoint)

def createSubmission(problemId , source):
    compilerId = 1
    response = None
    try:
        response = client.submissions.create(problemId, source , compilerId )
    # response['id'] stores the ID of the created submission
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
        elif e.code == 402:
            print('Unable to create submission')
        elif e.code == 400:
            print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))
    
    submissionID = response['id']
    try:
        response = client.submissions.get(submissionID)
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
        elif e.code == 403:
            print('Access to the submission is forbidden')
        elif e.code == 404:
            print('Submission does not exist')

    
    if response is not None:
        return response
    else:
        return 'An error Occured'
    