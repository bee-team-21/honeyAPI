from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.validators.mongo import PyObjectId
from typing import Literal, Optional
from pydantic import BaseModel
from pydantic.fields import Field


class Sites(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    type: Literal['M', 'F', 'Z','']
    city: Optional[str]
    country: Optional[str]
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
