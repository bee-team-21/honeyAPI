from app.core.database import db
from app.models.discord import Discord
from datetime import datetime
from pymongo.collection import ReturnDocument

def create(discord: Discord):
    discord.date_insert = datetime.utcnow()
    discord.disabled = False
    if hasattr(discord, "date_update"):
        delattr(discord, "date_update")
    if hasattr(discord, "id"):
        delattr(discord, "id")
    if hasattr(discord, "username_update"):
        delattr(discord, "username_update")
    ret = db.discord.insert_one(discord.dict(by_alias=True))
    return ret

def update(discord: Discord):
    if hasattr(discord, "date_insert"):
        delattr(discord, "date_insert")
    if hasattr(discord, "disabled"):
        delattr(discord, "disabled")
    if hasattr(discord, "username_insert"):
        delattr(discord, "username_insert")
    discord.date_update = datetime.utcnow()
    ret = db.discord.find_one_and_update(
        {"_id": discord.id, "disabled": False},
        {"$set": discord.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def delete(discord: Discord):
    discord.date_update = datetime.utcnow()
    ret = db.discord.find_one_and_update(
        {"_id": discord.id, "disabled": False},
        {"$set": {"disabled": True, "date_update": discord.date_update, "username_update": discord.username_update}},
        return_document=ReturnDocument.AFTER,
    )
    return ret


def getByID(discord: Discord):
    finded = db.discord.find_one({"_id": discord.id, "disabled": False})
    if finded is not None:
        return Discord(**finded)
    else:
        return None


def get():
    finded = db.discord.find({"disabled": False})
    discords = []
    for find in finded:
        discords.append(Discord(**find))
    return discords

def search(discord: Discord):
    finded = db.discord.find(
        {
            "$and": [
                {"disabled": False},
                {
                    "$or": [
                        {"segment": {"$regex": discord.segment, "$options": "i"}},
                        {"name": {"$regex": discord.name, "$options": "i"}},
                    ]
                },
            ]
        }
    )
    discords = []
    for find in finded:
        discords.append(Discord(**find))
    return discords


def update_segment(oldsegment: str, newsegment: str):
    ret = db.discord.update_many(
        {"segment": oldsegment, "disabled": False},
        {"$set": {"segment": newsegment}},
    )
    return ret


def get_by_segment(item: Discord):
    finded = db.discord.find({"segment": item.segment, "disabled": False})
    items = []
    for find in finded:
        items.append(Discord(**find))
    return items