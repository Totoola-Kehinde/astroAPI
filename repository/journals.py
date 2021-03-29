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

    def read(self, journal_id): 
        try:
            return db.journals.find({"journal_id":journal_id})
        except pymongo.errors.NetworkTimeout as e:
            error_msg = "Error :{}".format(e)
            return error_msg