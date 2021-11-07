from typing import List
from app.core.database import db
from app.models.sites_model import Sites
from datetime import datetime
from pymongo.collection import ReturnDocument


def create(item: Sites):
    item.date_insert = datetime.utcnow()
    item.disabled = False
    if hasattr(item, "date_update"):
        delattr(item, "date_update")
    if hasattr(item, "id"):
        delattr(item, "id")
    if hasattr(item, "username_update"):
        delattr(item, "username_update")
    ret = db.sites.insert_one(item.dict(by_alias=True))
    return ret


def update(item: Sites):
    if hasattr(item, "date_insert"):
        delattr(item, "date_insert")
    if hasattr(item, "username_insert"):
        delattr(item, "username_insert")
    if hasattr(item, "disabled"):
        delattr(item, "disabled")
    item.date_update = datetime.utcnow()
    ret = db.sites.find_one_and_update(
        {"_id": item.id, "disabled": False},
        {"$set": item.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def delete(item: Sites):
    item.date_update = datetime.utcnow()
    ret = db.sites.find_one_and_update(
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


def getByID(item: Sites):
    finded = db.sites.find_one({"_id": item.id, "disabled": False})
    if finded is not None:
        return Sites(**finded)
    else:
        return None


def get():
    finded = db.sites.find({"disabled": False})
    items = []
    for find in finded:
        items.append(Sites(**find))
    return items

def getByName(item: Sites) -> List[Sites]:
    finded = db.sites.find({"name": item.name, "disabled": False})
    items = []
    for find in finded:
        items.append(Sites(**find))
    return items

def getByNameAndNotID(item: Sites):
    finded = db.sites.find({"name": item.name, "disabled": False, "_id" : {"$not": {"$eq": item.id}}})
    items = []
    for find in finded:
        items.append(Sites(**find))
    return items


def search(item: Sites):
    if item.type == "":
        finded = db.sites.find(
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
    else:
        finded = db.sites.find(
        {
            "$and": [
                {"disabled": False},
                {"type": item.type},
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
        items.append(Sites(**find))
    return items
