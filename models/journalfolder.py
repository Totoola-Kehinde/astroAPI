from pydantic import BaseModel, Field, EmailStr
import datetime

class journalfolder(BaseModel):
    """ Collection Of Journals """

    title: str = Field(default=None)
    journal_ids : list = Field(default=None)
    created_at: datetime.datetime = Field(default=None)
    updated_at: datetime.datetime = Field(default=None)