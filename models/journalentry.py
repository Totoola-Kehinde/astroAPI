from pydantic import BaseModel, Field, EmailStr
import datetime

class journalentry(BaseModel):
    """ Collection Of Journal Entries """

    journal_title: str = Field(default=None)
    created_at: datetime.datetime = Field(default=None)
    note: str = Field(None, title="Tell us how your day went", max_length=2000)
    updated_at: datetime.datetime = Field(default=None)