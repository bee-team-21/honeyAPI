from datetime import datetime
from bson import ObjectId
from app.validators.mongo import PyObjectId
from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class Token(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    token: str
    disabled: Optional[bool] = False
    date_insert: Optional[datetime] = None
    date_update: Optional[datetime] = None
    username_insert: Optional[str] = None
    username_update: Optional[str] = None
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
