from datetime import datetime
from bson import ObjectId
from app.validators.mongo import PyObjectId
from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class Slack(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    segment: str
    name: Optional[str] = None
    token: str
    channel: str
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
