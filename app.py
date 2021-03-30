from fastapi import FastAPI, Depends
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field
from repository.users import users
from repository.journals import journals
from models.user import user, userlogin
from models.journalfolder import journalfolder
from models.journalentry import journalentry
from controllers.check import email_exists, checkhashpassword, checklogincred
from controllers.hashpassword import hashpassword
from controllers.time import created_at
from auth.auth_handler import signJWT, decodeJWT
from auth.auth_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson.json_util import dumps
import json
from typing import Optional


app = FastAPI(
    title="Therapy API",
    description="A simple Therapy API in FastAPI",
    version="0.1",
)

userscontroller = users()
journalscontroller = journals()

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

class journalId(BaseModel):
    id: Optional[ObjectIdStr] = Field(alias='_id')


@app.get("/")
def home():
    return{"home":"Homepage"}

@app.post("/user/signup", tags=['user'])
def create_user( User:user):
    if email_exists(User.email) == False:
        User.password = hashpassword(User.password)
        newuser = user(id = ObjectId(), name=User.name, email=User.email, password=User.password, created_at=User.created_at)

        userscontroller.create(newuser)
        return JSONResponse(content=signJWT(User.id, User.email))

    return{'Message':'User Already Exists!'}

@app.post("/user/reset", tags=['user'])
def reset_password( User:user):
    if email_exists(User.email) == False:
        return {'Message':"I dey come"}

    return{'Message':'User Already Exists!'}


@app.post("/user/login", tags=['user'])
def login(User:userlogin):
    checkuser: bool
    checkuser = email_exists(User.email)

    if checkuser == True:
        # If password is correct
        if checkhashpassword(User): 
            if checklogincred:
                active_user = userscontroller.read(User.email)
                print(active_user)
                active = dumps(active_user)
                active = json.loads(active)
                active_user_id = active[0]['_id']
                active_user_id = active_user_id['$oid']
                print(active_user_id)
                active_user_email = active[0]['email']
                result = signJWT(active_user_id, active_user_email)
                print(result)
                return JSONResponse(content=result)
        return JSONResponse(content={"message":"Incorrect Password"})
    return JSONResponse(content={"Message":"User does not exist OR incorrect email"})

def get_active_user(token: str = Depends(JWTBearer())):
    payload = decodeJWT(token)
    return payload

def get_current_active_user(current_user: user = Depends(get_active_user)):
    return current_user

@app.get("/user/me", dependencies=[Depends(JWTBearer())], tags=['user'])
def current_user(current_user: user = Depends(get_current_active_user)):
    # activeuser = decodeJWT(token)
    return JSONResponse(content={"Active User":current_user})


@app.post("/journal", dependencies=[Depends(JWTBearer())], tags=['journal'])
def create_journal(journal_id: int, journal:journalentry, journal_user: user = Depends(get_current_active_user)):
    # token = decodeJWT(token)
    newjournal = journalentry(id = ObjectId(), journal_id=journal_id, owner=journal_user['user_id'], journal_title=journal.journal_title, created_at=created_at(), note=journal.note, updated_at=None)

    journalscontroller.create(newjournal)
    return JSONResponse(content={"Message":"New Journal Created"})



@app.get("/journal/{journal_id}", dependencies=[Depends(JWTBearer())], tags=['journal'])
def get_journal(journal_id: int, journal_user: user = Depends(get_current_active_user)):
    result = journalscontroller.read(journal_id, journal_user['user_id'])
    result = dumps(result)

    return JSONResponse(content={"message":result})


@app.get("/journal/all", dependencies=[Depends(JWTBearer())], response_model=journalentry, tags=['user journal'])
def get_all_journal(journal_user: user = Depends(get_current_active_user)):
    result = journalscontroller.read(int(0), journal_user['user_id'])
    return JSONResponse(content={"message":result})