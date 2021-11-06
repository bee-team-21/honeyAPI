from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.models.user import UserInDB
from app.models.history import History
from app.models.result import Result
from app.access import get_actual_user
from app.services import history_service, segment_service
from app.validators.mongo import PyObjectId
from app.utils.responses import KEYS_ERROR
from app.utils.result import get_error

router = APIRouter()

# @router.post(
#     "",
#     response_model=History,
#     status_code=status.HTTP_201_CREATED,
#     responses={
#         status.HTTP_201_CREATED: {"model": History},
#         status.HTTP_409_CONFLICT: {"model": Result},
#     },
# )
# async def post_history(
#     item: History, user: Optional[UserInDB] = Depends(get_actual_user)
# ):
#     if hasattr(item, "username_insert"):
#         delattr(item, "username_insert")
#     if hasattr(item, "id"):
#         delattr(item, "id")
#     if hasattr(item, "username_update"):
#         delattr(item, "username_update")

    
#     item.username_insert = user.username
#     ret = history_service.create(item)
#     item.id = ret.inserted_id
#     ret = history_service.getByID(item)
#     return ret

@router.get("", response_model=List[History], status_code=status.HTTP_200_OK)
async def get_history(
    user: Optional[UserInDB] = Depends(get_actual_user), q: Optional[str] = None
):
    search = History(plataform="", username_insert="", request_payload="", activator="")
    if q is not None:
        search.plataform = q
        search.username_insert = q
        search.request_payload = q
        search.activator = q
        historys = history_service.search(history=search)
    else:
        historys = history_service.get()
    return historys
