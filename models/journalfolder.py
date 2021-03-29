from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import datetime

class journalfolder(BaseModel):
    """ Collection Of Journals """

    title: str = Field(default=None)
    journal_ids : Optional[list] = Field(default=None)
    created_at: datetime.datetime = Field(default=None)
    updated_at: datetime.datetime = Field(default=None)