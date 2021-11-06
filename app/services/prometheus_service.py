from inspect import trace
import traceback
from app.core.database import db
from app.models.prometheus import AlertmanagerInDB
from datetime import datetime

def create(item: AlertmanagerInDB):
    try:
        item.date_insert = datetime.utcnow()
        item.disabled = False
        if hasattr(item, "date_update"):
            delattr(item, "date_update")
        if hasattr(item, "id"):
            delattr(item, "id")
        if hasattr(item, "username_update"):
            delattr(item, "username_update")
        ret = db.prometheus.insert_one(item.dict(by_alias=True))
        return ret
    except:
        traceback.print_exc()
        return None