from app.core.database import db
from app.models.phone import Phone
from datetime import datetime
from pymongo.collection import ReturnDocument

def create(phone: Phone):
    phone.date_insert = datetime.utcnow()
    phone.disabled = False
    if hasattr(phone, "date_update"):
        delattr(phone, "date_update")
    if hasattr(phone, "id"):
        delattr(phone, "id")
    if hasattr(phone, "username_update"):
        delattr(phone, "username_update")
    ret = db.phone.insert_one(phone.dict(by_alias=True))
    return ret

def update(phone: Phone):
    if hasattr(phone, "date_insert"):
        delattr(phone, "date_insert")
    if hasattr(phone, "disabled"):
        delattr(phone, "disabled")
    if hasattr(phone, "username_insert"):
        delattr(phone, "username_insert")
    phone.date_update = datetime.utcnow()
    ret = db.phone.find_one_and_update(
        {"_id": phone.id, "disabled": False},
        {"$set": phone.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def delete(phone: Phone):
    phone.date_update = datetime.utcnow()
    ret = db.phone.find_one_and_update(
        {"_id": phone.id, "disabled": False},
        {"$set": {"disabled": True, "date_update": phone.date_update, "username_update": phone.username_update}},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def getByID(phone: Phone):
    finded = db.phone.find_one({"_id": phone.id, "disabled": False})
    if finded is not None:
        return Phone(**finded)
    else:
        return None


def get():
    finded = db.phone.find({"disabled": False})
    phones = []
    for find in finded:
        phones.append(Phone(**find))
    return phones

def search(phone: Phone):
    finded = db.phone.find(
        {
            "$and": [
                {"disabled": False},
                {
                    "$or": [
                        {"segment": {"$regex": phone.segment, "$options": "i"}},
                        {"number": {"$regex": phone.number}},
                        {"name": {"$regex": phone.name, "$options": "i"}},
                    ]
                },
            ]
        }
    )
    phones = []
    for find in finded:
        phones.append(Phone(**find))
    return phones


def update_segment(oldsegment: str, newsegment: str):
    ret = db.phone.update_many(
        {"segment": oldsegment, "disabled": False},
        {"$set": {"segment": newsegment}},
    )
    return ret


def get_by_segment(item: Phone):
    finded = db.phone.find({"segment": item.segment, "disabled": False})
    items = []
    for find in finded:
        items.append(Phone(**find))
    return items