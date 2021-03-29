from fastapi import FastAPI, Depends
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field
from repository.users import users
from models.user import user, userlogin
from controllers.check import email_exists
from controllers.hashpassword import hashpassword
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
from typing import Optional


app = FastAPI()

userscontroller = users()


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)

class userId(BaseModel):
    id: Optional[ObjectIdStr] = Field(alias='_id')



@app.get("/")
def home():
    return{"home":"Homepage"}

message = ''
@app.post("/user/signup", tags=['user'])
def create_user( User:user):
    if email_exists(User.email) == False:
        User.password = hashpassword(User.password)
        newuser = user(id = ObjectId(), name=User.name, email=User.email, password=User.password, dt=User.dt)

        userscontroller.create(newuser)
        message = signJWT(User.email)

    elif email_exists(User.email) == True:
        message = 'User Already Exists!'
    return message



@app.post("/user/login", tags=['user'])
def login(User:userlogin):
    checkuser = True
    checkuser = email_exists(User.email)

    if checkuser == True:
        return{"Message":"User does not exist OR incorrect email"}

