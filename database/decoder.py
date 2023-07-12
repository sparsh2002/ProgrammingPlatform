from flask.json import JSONEncoder
from bson.objectid import ObjectId
class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)