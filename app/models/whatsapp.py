from typing import List, Optional, Union
from app.validators.mongo import PyObjectId
from bson import ObjectId
from pydantic import BaseModel
from pydantic.fields import Field
from datetime import datetime

class WhatsApp(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    group_id: str
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

class WhatsAppNotifyText(BaseModel):
    text: str
class WhatsAppNotifyImage(BaseModel):
    url: str
    caption: str
    filename: str ="image.png"
class WhatsAppNotify(BaseModel):
    segment: str
    messages: List[Union[WhatsAppNotifyText, WhatsAppNotifyImage]] = []
