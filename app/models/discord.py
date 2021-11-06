from typing import List, Optional, Union
from app.validators.mongo import PyObjectId
from bson import ObjectId
from pydantic import BaseModel
from pydantic.fields import Field
from datetime import datetime

class Discord (BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    channel_webhook: str
    segment: str  
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


class DiscordFileUrl(BaseModel):
    url: str
    header: Optional[str] = None
    header_content: Optional[str] = None

class DiscordMessage(BaseModel):
    text: str
    file: Optional[DiscordFileUrl] = None

class DiscordNotify(BaseModel):
    segment: str
    messages: List[DiscordMessage] = []