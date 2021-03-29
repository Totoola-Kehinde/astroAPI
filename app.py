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
from auth.auth_handler import signJWT, decodeJWT
from auth.auth_bearer import JWTBearer
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
        return signJWT(User.email)

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
                return signJWT(User.email)
        return{"message":"Incorrect Password"}
    return{"Message":"User does not exist OR incorrect email"}


@app.get("/user/me", dependencies=[Depends(JWTBearer())], tags=['user'])
def current_user(token: str):
    activeuser = decodeJWT(token)
    return {"Active User": activeuser}


@app.post("/journal", dependencies=[Depends(JWTBearer())], tags=['journal'])
def create_journal(journal_id: int, token, journal:journalentry):
    token = decodeJWT(token)
    newjournal = journalentry(id = ObjectId(), journal_id=journal_id, owner=token['user_id'], journal_title=journal.journal_title, created_at=journal.created_at, note=journal.note, updated_at=None)

    journalscontroller.create(newjournal)
    return {"Message":"New Journal Created", "Created at":newjournal.created_at}



@app.get("/journal/{journal_id}", dependencies=[Depends(JWTBearer())], tags=['journal'])
def get_journal(journal_id:int, token):
    token = decodeJWT(token)
    return journalscontroller.read(journal_id, token['user_id'])