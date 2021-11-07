from app.core.database import db
from app.models.AnalizysResult_model import AnalysisResult
from datetime import datetime
from pymongo.collection import ReturnDocument

def create(item: AnalysisResult):
    item.date_insert = datetime.utcnow()
    item.disabled = False
    if hasattr(item, "date_update"):
        delattr(item, "date_update")
    if hasattr(item, "id"):
        delattr(item, "id")
    if hasattr(item, "username_update"):
        delattr(item, "username_update")
    ret = db.analysis.insert_one(item.dict(by_alias=True))
    return ret