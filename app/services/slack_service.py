from app.core.database import db
from app.models.slack import Slack
from datetime import datetime
from pymongo.collection import ReturnDocument


def create(item: Slack):
    item.date_insert = datetime.utcnow()
    item.disabled = False
    if hasattr(item, "date_update"):
        delattr(item, "date_update")
    if hasattr(item, "id"):
        delattr(item, "id")
    if hasattr(item, "username_update"):
        delattr(item, "username_update")
    ret = db.slack.insert_one(item.dict(by_alias=True))
    return ret


def update(item: Slack):
    if hasattr(item, "date_insert"):
        delattr(item, "date_insert")
    if hasattr(item, "username_insert"):
        delattr(item, "username_insert")
    if hasattr(item, "disabled"):
        delattr(item, "disabled")
    item.date_update = datetime.utcnow()
    ret = db.slack.find_one_and_update(
        {"_id": item.id, "disabled": False},
        {"$set": item.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def delete(item: Slack):
    item.date_update = datetime.utcnow()
    ret = db.slack.find_one_and_update(
        {"_id": item.id, "disabled": False},
        {
            "$set": {
                "disabled": True,
                "date_update": item.date_update,
                "username_update": item.username_update,
            }
        },
        return_document=ReturnDocument.AFTER,
    )
    return ret


def get_by_ID(item: Slack):
    finded = db.slack.find_one({"_id": item.id, "disabled": False})
    if finded is not None:
        return Slack(**finded)
    else:
        return None

def get_by_segment(item: Slack):
    finded = db.slack.find({"segment": item.segment, "disabled": False})
    items = []
    for find in finded:
        items.append(Slack(**find))
    return items


def get():
    finded = db.slack.find({"disabled": False})
    items = []
    for find in finded:
        items.append(Slack(**find))
    return items


def search(item: Slack):
    finded = db.slack.find(
        {
            "$and": [
                {"disabled": False},
                {
                    "$or": [
                        {"token": {"$regex": item.token}},
                        {"name": {"$regex": item.name, "$options": "i"}},
                    ]
                },
            ]
        }
    )
    items = []
    for find in finded:
        items.append(Slack(**find))
    return items


def update_segment(oldsegment: str, newsegment: str):
    ret = db.slack.update_many(
        {"segment": oldsegment, "disabled": False},
        {"$set": {"segment": newsegment}},
    )
    return ret
