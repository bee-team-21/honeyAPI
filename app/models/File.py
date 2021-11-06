
from datetime import datetime
from typing import Optional
from pydantic.main import BaseModel
from bson import ObjectId
from pydantic.fields import Field
from app.validators.mongo import PyObjectId

class File(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    file: bytes = None
    filename: str = None
    mimetype: str = None
    date_insert: Optional[datetime] = None
    disabled: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }