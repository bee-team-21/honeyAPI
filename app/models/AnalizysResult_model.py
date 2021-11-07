from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

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

class AnalysisResult(BaseModel):
    user_id : str
    image_url: str
    tags:List[Tag]
    captions:Optional[List[Captions]]
    risk: List[Risk]
    text: Optional[str]
    text_en: Optional[str]
    site: Optional[str]
    site_gps: Optional[str]
    disabled: Optional[bool] = False
    date_insert: Optional[datetime] = None
    date_update: Optional[datetime] = None
    username_insert: Optional[str] = None
    username_update: Optional[str] = None