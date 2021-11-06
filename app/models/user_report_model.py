from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.validators.mongo import PyObjectId
from typing import Literal, Optional, Union
from pydantic import BaseModel
from pydantic.fields import Field


class UserReportBot(BaseModel):
    imageType: str
    image: str
    gps: Optional[Union[dict,str]] = None
    site: Optional[str]

class UserReportResponse(BaseModel):
    detail: Optional[str]

class UserReport(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    url: str
    id_site: Optional[PyObjectId]
    lat: Optional[float] = 0.0
    long: Optional[float] = 0.0
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
