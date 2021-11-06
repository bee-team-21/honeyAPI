from datetime import datetime
from app.core.database import db
from app.models.File import File

def create(item: File):
    if hasattr(item, "id"):
        delattr(item, "id")
    item.date_insert = datetime.utcnow()
    ret = db.file.insert_one(item.dict(by_alias=True))
    return ret

def get():
    finded = db.file.find({"disabled": False}, { 'filename': 1, 'mimetype': 1 , 'date_insert': 1} )
    items = []
    for find in finded:
        items.append(File(**find))
    return items
    
def search(item: File):
    finded = db.file.find(
        {
            "$and": [
                {"disabled": False},
                {
                    "$or": [
                        {"filename": {"$regex": item.filename, "$options": "i"}},
                        {"mimetype": {"$regex": item.mimetype, "$options": "i"}},
                    ]
                },
            ]
        }
    )
    items = []
    for find in finded:
        items.append(File(**find))
    return items


def getByID(item: File):
    finded = db.file.find_one({"_id": item.id})
    if finded is not None:
        return File(**finded)
    else:
        return None