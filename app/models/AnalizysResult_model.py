from typing import List, Optional
from bson.objectid import ObjectId
from pydantic import BaseModel
from datetime import datetime

from pydantic.fields import Field

from app.validators.mongo import PyObjectId

class Tag(BaseModel):
    name:str
    score: float
    flg_animal: Optional[bool] = False
    flg_cage: Optional[bool] = False

class Captions(BaseModel):
    text : str
    confidence:float

class Risk(BaseModel):
    grade: str
    confidence: float

class DetectedObjects(BaseModel):
    name:  Optional[str]
    confidence:  Optional[float]
    flg_animal: Optional[bool] = False
class AnalysisResult(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id : str
    image_url: str
    tags:List[Tag]
    detected_objects : Optional[List[DetectedObjects]]
    captions:Optional[List[Captions]]
    risk: List[Risk]
    text: Optional[str]
    text_en: Optional[str]
    site: Optional[str]
    site_gps: Optional[str]
    id_site: Optional[PyObjectId] = None
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