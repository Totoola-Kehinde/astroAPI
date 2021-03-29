from pydantic import BaseModel, Field, EmailStr
import datetime

class journalfolder(BaseModel):
    """ Collection Of Journals """

    title: str = Field(default=None)
    createdat: datetime.datetime = Field(default=None)
    updatedat: datetime.datetime = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "title": "Monday January 2021",
                "createdat": datetime.datetime,
                "updatedat": datetime.datetime
            }
        }