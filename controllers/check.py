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

def checkhashpassword(userinput):
    valid = False
    user  = db.users.find({'email': userinput.email})
    if hashpassword(userinput.password) == user.password:
        valid = True
    elif hashpassword(userinput.password) is not user.password:
        valid = False
    return valid

def checklogincred(userinput):
    validlogin = True
    user = db.users.find({'email': userinput.email})
    if userinput.email == user.email and hashpassword(userinput.password) == user.password:
        validlogin = True
    else:
        validlogin = False
    return validlogin