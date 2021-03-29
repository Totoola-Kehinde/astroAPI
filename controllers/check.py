from pymongo import MongoClient
from .hashpassword import hashpassword
from models.user import userlogin
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
    return user_exist

def checkhashpassword(userinput: userlogin):
    valid = False
    user  = db.users.find_one({'email': userinput.email})
    if hashpassword(userinput.password) == user['password']:
        valid = True
    elif hashpassword(userinput.password) is not user['password']:
        valid = False
    return valid

def checklogincred(userinput):
    user = db.users.find_one({'email': userinput.email})
    if userinput.email == user['email'] and checkhashpassword(userinput.password):
        return True
    else:
        return False