# this is the middle ware to distinguish between user and admin
import os
from dotenv import load_dotenv
from database.conn import client as dbclient
load_dotenv()
db = dbclient['cometlabs']
def getRole(userId):

    users = db.users
    user = users.find_one({"id":userId})

    return user['role']