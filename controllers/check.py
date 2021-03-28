from pymongo import MongoClient
from .hashpassword import hashpassword
import settings

client =  MongoClient(settings.MONGODB_URI)
db =  client[settings.MONGODB_DATABASE]

def email_exists(email):
    user_exist = True
    if db.users.find(
        {'email': email}
    ).count() == 0:
        user_exist = False
        return user_exist

def checkhashpassword(userinput, password):
    valid = False
    if hashpassword(userinput) == password:
        valid = True
    elif hashpassword(userinput) is not password:
        valid = False
    return valid