import pymongo
from pymongo import MongoClient
from models.user import user
from bson.objectid import ObjectId
import settings

client =  MongoClient(settings.MONGODB_URI)
db =  client[settings.MONGODB_DATABASE]

class users(user):
    """ User model used in writing and reading from MongoDB """

    error_msg = str
    
    def create(self, user):
        if user is not None:
            try:
                return db.users.insert_one(dict(user))
            except pymongo.errors.NetworkTimeout as e:
                error_msg = "Error :{}".format(e)
                return self.error_msg
        else:
            return Exception("Nothing to save, because wiseword parameter is None")

    def read(self, email): 
        try:
            return db.users.find({"email":email})
        except pymongo.errors.NetworkTimeout as e:
            error_msg = "Error :{}".format(e)
            return error_msg