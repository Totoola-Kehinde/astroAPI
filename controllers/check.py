from pymongo import MongoClient
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