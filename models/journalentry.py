from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import datetime

class journalentry(BaseModel):
    """ Collection Of Journal Entries """

    title: str = Field(default=None)
    createdat: datetime.datetime = Field(default=None)
    note: Optional[str] = Field(
        None, title="Tell us how your day went", max_length=2000
    )
    updatedat: datetime.datetime = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "title": "Today went fine...a bit",
                "createdat": datetime.datetime,
                "note": "Tell us how your day went",
                "updatedat": datetime.datetime
            }
        }