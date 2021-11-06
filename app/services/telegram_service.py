from app.core.database import db
from app.models.telegram import Telegram
from datetime import datetime
from pymongo.collection import ReturnDocument

def create(telegram: Telegram):
    telegram.date_insert = datetime.utcnow()
    telegram.disabled = False
    if hasattr(telegram, "date_update"):
        delattr(telegram, "date_update")
    if hasattr(telegram, "id"):
        delattr(telegram, "id")
    if hasattr(telegram, "username_update"):
        delattr(telegram, "username_update")
    ret = db.telegram.insert_one(telegram.dict(by_alias=True))
    return ret

def update(telegram: Telegram):
    if hasattr(telegram, "date_insert"):
        delattr(telegram, "date_insert")
    if hasattr(telegram, "disabled"):
        delattr(telegram, "disabled")
    if hasattr(telegram, "username_insert"):
        delattr(telegram, "username_insert")
    telegram.date_update = datetime.utcnow()
    ret = db.telegram.find_one_and_update(
        {"_id": telegram.id, "disabled": False},
        {"$set": telegram.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def delete(telegram: Telegram):
    telegram.date_update = datetime.utcnow()
    ret = db.telegram.find_one_and_update(
        {"_id": telegram.id, "disabled": False},
        {"$set": {"disabled": True, "date_update": telegram.date_update, "username_update": telegram.username_update}},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def getByID(telegram: Telegram):
    finded = db.telegram.find_one({"_id": telegram.id, "disabled": False})
    if finded is not None:
        return Telegram(**finded)
    else:
        return None


def get():
    finded = db.telegram.find({"disabled": False})
    telegrams = []
    for find in finded:
        telegrams.append(Telegram(**find))
    return telegrams

def search(telegram: Telegram):
    finded = db.telegram.find(
        {
            "$and": [
                {"disabled": False},
                {
                    "$or": [
                        {"segment": {"$regex": telegram.segment, "$options": "i"}},
                        {"chat_id": {"$regex": telegram.chat_id}},
                        {"name": {"$regex": telegram.name, "$options": "i"}},
                    ]
                },
            ]
        }
    )
    telegrams = []
    for find in finded:
        telegrams.append(Telegram(**find))
    return telegrams


def update_segment(oldsegment: str, newsegment: str):
    ret = db.telegram.update_many(
        {"segment": oldsegment, "disabled": False},
        {"$set": {"segment": newsegment}},
    )
    return ret


def get_by_segment(item: Telegram):
    finded = db.telegram.find({"segment": item.segment, "disabled": False})
    items = []
    for find in finded:
        items.append(Telegram(**find))
    return items