import pymongo
from pymongo import MongoClient
from models.journalentry import journalentry
from bson.objectid import ObjectId
import settings

client =  MongoClient(settings.MONGODB_URI)
db =  client[settings.MONGODB_DATABASE]

class journals(journalentry):
    """ Journal model used in writing and reading from MongoDB """

    error_msg = str
    
    def create(self, journal):
        if journal is not None:
            try:
                return db.journals.insert_one(dict(journal))
            except pymongo.errors.NetworkTimeout as e:
                error_msg = "Error :{}".format(e)
                return error_msg
        else:
            return Exception("Nothing to save, because journal parameter is None")

    def read(self, journa_id, owner):
        try:
            if journa_id == 0:
                return db.journals.find({"owner":{"$eq":owner}})
            return db.journals.find_one({"journal_id":{"$eq":journa_id}, "owner":owner})
        except pymongo.errors.NetworkTimeout as e:
            error_msg = "Error :{}".format(e)
            return error_msg