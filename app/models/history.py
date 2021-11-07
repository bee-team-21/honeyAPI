from datetime import datetime
from bson import ObjectId
from app.validators.mongo import PyObjectId
from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field

class Plataform:
    slack = "slack"
    whatsapp = "whatsapp"
    sms = "sms"
    telegram = "telegram"
    discord = "discord"

class History(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    date_insert: Optional[datetime] = None
    username_insert: Optional[str] = None
    request_payload: Optional[str] = None
    response_code: Optional[int] = 0
    response_text: Optional[str] = None
    activator: Optional[str] = None
    plataform: Optional[str] = None
    disabled: Optional[bool] = False
    image: Optional[str] = None
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }