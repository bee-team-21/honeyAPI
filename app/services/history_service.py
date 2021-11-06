from app.core.database import db
from app.models.history import History
from datetime import datetime



def create(item: History):
    item.date_insert = datetime.utcnow()
    item.disabled = False
    if hasattr(item, "date_update"):
        delattr(item, "date_update")
    if hasattr(item, "id"):
        delattr(item, "id")
    if hasattr(item, "username_update"):
        delattr(item, "username_update")
    ret = db.history.insert_one(item.dict(by_alias=True))
    return ret

def get():
    finded = db.history.find({"disabled": False})
    items = []
    for find in finded:
        items.append(History(**find))
    return items

def search(history: History):
    finded = db.history.find(
        {
            "$and": [
                {"disabled": False},
                {
                    "$or": [
                        {"plataform": {"$regex": history.plataform, "$options": "i"}},
                        {"username_insert": {"$regex": history.username_insert}},
                        {"request_payload": {"$regex": history.request_payload, "$options": "i"}},
                        {"activator": {"$regex": history.activator, "$options": "i"}},
                    ]
                },
            ]
        }
    )
    historys = []
    for find in finded:
        historys.append(History(**find))
    return historys