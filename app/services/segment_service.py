from typing import Literal
from app.core.database import db
from app.models.segment import Segment
from datetime import datetime
from pymongo.collection import ReturnDocument


def create(item: Segment):
    item.date_insert = datetime.utcnow()
    item.disabled = False
    if hasattr(item, "date_update"):
        delattr(item, "date_update")
    if hasattr(item, "id"):
        delattr(item, "id")
    if hasattr(item, "username_update"):
        delattr(item, "username_update")
    ret = db.segment.insert_one(item.dict(by_alias=True))
    return ret


def update(item: Segment):
    if hasattr(item, "date_insert"):
        delattr(item, "date_insert")
    if hasattr(item, "username_insert"):
        delattr(item, "username_insert")
    if hasattr(item, "disabled"):
        delattr(item, "disabled")
    item.date_update = datetime.utcnow()
    ret = db.segment.find_one_and_update(
        {"_id": item.id, "disabled": False},
        {"$set": item.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def delete(item: Segment):
    item.date_update = datetime.utcnow()
    ret = db.segment.find_one_and_update(
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


def getByID(item: Segment):
    finded = db.segment.find_one({"_id": item.id, "disabled": False})
    if finded is not None:
        return Segment(**finded)
    else:
        return None


def get():
    finded = db.segment.find({"disabled": False})
    items = []
    for find in finded:
        items.append(Segment(**find))
    return items

def getByName(item: Segment):
    finded = db.segment.find({"name": item.name, "disabled": False})
    items = []
    for find in finded:
        items.append(Segment(**find))
    return items

def getByNameAndNotID(item: Segment):
    finded = db.segment.find({"name": item.name, "disabled": False, "_id" : {"$not": {"$eq": item.id}}})
    items = []
    for find in finded:
        items.append(Segment(**find))
    return items


def search(item: Segment):
    finded = db.segment.find(
        {
            "$and": [
                {"disabled": False},
                {
                    "$or": [
                        {"name": {"$regex": item.name, "$options": "i"}},
                    ]
                },
            ]
        }
    )
    items = []
    for find in finded:
        items.append(Segment(**find))
    return items

def getByRisk(risk: Literal['low','mid','high']):
    finded = db.segment.find(
        {
            "$and": [
                {"disabled": False},
                {"risk": risk},
            ]
        }
    )
    items = []
    for find in finded:
        items.append(Segment(**find))
    return items