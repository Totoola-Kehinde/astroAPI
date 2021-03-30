from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import datetime


class user(BaseModel):
    """ Collection Of Users """
    id : Optional[str] = None
    name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    created_at: datetime.datetime = Field(default=None)

class userlogin(BaseModel):

    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "email": "totoolakenny@gmail.com",
                "password": "weakpassword"
            }
        }