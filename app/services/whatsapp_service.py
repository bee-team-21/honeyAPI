from app.core.database import db
from app.models.whatsapp import WhatsApp
from datetime import datetime
from pymongo.collection import ReturnDocument

def create(whatsapp: WhatsApp):
    whatsapp.date_insert = datetime.utcnow()
    whatsapp.disabled = False
    if hasattr(whatsapp, "date_update"):
        delattr(whatsapp, "date_update")
    if hasattr(whatsapp, "id"):
        delattr(whatsapp, "id")
    if hasattr(whatsapp, "username_update"):
        delattr(whatsapp, "username_update")
    ret = db.whatsapp.insert_one(whatsapp.dict(by_alias=True))
    return ret

def update(whatsapp: WhatsApp):
    if hasattr(whatsapp, "date_insert"):
        delattr(whatsapp, "date_insert")
    if hasattr(whatsapp, "disabled"):
        delattr(whatsapp, "disabled")
    if hasattr(whatsapp, "username_insert"):
        delattr(whatsapp, "username_insert")
    whatsapp.date_update = datetime.utcnow()
    ret = db.whatsapp.find_one_and_update(
        {"_id": whatsapp.id, "disabled": False},
        {"$set": whatsapp.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def delete(whatsapp: WhatsApp):
    whatsapp.date_update = datetime.utcnow()
    ret = db.whatsapp.find_one_and_update(
        {"_id": whatsapp.id, "disabled": False},
        {"$set": {"disabled": True, "date_update": whatsapp.date_update, "username_update": whatsapp.username_update}},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def getByID(whatsapp: WhatsApp):
    finded = db.whatsapp.find_one({"_id": whatsapp.id, "disabled": False})
    if finded is not None:
        return WhatsApp(**finded)
    else:
        return None


def get():
    finded = db.whatsapp.find({"disabled": False})
    whatsapps = []
    for find in finded:
        whatsapps.append(WhatsApp(**find))
    return whatsapps

def search(whatsapp: WhatsApp):
    finded = db.whatsapp.find(
        {
            "$and": [
                {"disabled": False},
                {
                    "$or": [
                        {"segment": {"$regex": whatsapp.segment, "$options": "i"}},
                        {"group_id": {"$regex": whatsapp.group_id}},
                        {"name": {"$regex": whatsapp.name, "$options": "i"}},
                    ]
                },
            ]
        }
    )
    whatsapps = []
    for find in finded:
        whatsapps.append(WhatsApp(**find))
    return whatsapps


def update_segment(oldsegment: str, newsegment: str):
    ret = db.whatsapp.update_many(
        {"segment": oldsegment, "disabled": False},
        {"$set": {"segment": newsegment}},
    )
    return ret


def get_by_segment(item: WhatsApp):
    finded = db.whatsapp.find({"segment": item.segment, "disabled": False})
    items = []
    for find in finded:
        items.append(WhatsApp(**find))
    return items