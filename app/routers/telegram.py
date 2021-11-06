from os import stat
from typing import List, Optional

from starlette.responses import Response
from fastapi import APIRouter, Depends, status

from app.models.user import UserInDB
from app.models.telegram import Telegram
from app.models.segment import Segment
from app.models.result import Result
from app.access import get_actual_user
from app.services import telegram_service, segment_service
from app.validators.mongo import PyObjectId
from app.utils.result import get_error
from app.utils.responses import KEYS_ERROR

router = APIRouter()


@router.get("", response_model=List[Telegram], status_code=status.HTTP_200_OK)
async def get_telegram(
    user: Optional[UserInDB] = Depends(get_actual_user), q: Optional[str] = None
):
    search = Telegram(name="", chat_id="", segment="")
    if q is not None:
        search.name = q
        search.chat_id = q
        search.segment = q
        telegrams = telegram_service.search(telegram=search)
    else:
        telegrams = telegram_service.get()
    return telegrams


@router.post(
    "",
    response_model=Telegram,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": Telegram},
        status.HTTP_409_CONFLICT: {"model": Result},
    },
)
async def post_telegram(
    item: Telegram, user: Optional[UserInDB] = Depends(get_actual_user)
):
    if hasattr(item, "username_insert"):
        delattr(item, "username_insert")
    if hasattr(item, "username_update"):
        delattr(item, "username_update")
    segment = Segment(name=item.segment)
    segments = segment_service.getByName(segment)
    if segments == []:
        return get_error(
            key=KEYS_ERROR.segment_not_found, status_code=status.HTTP_409_CONFLICT
        )
    item.username_insert = user.username
    ret = telegram_service.create(item)
    item.id = ret.inserted_id
    ret = telegram_service.getByID(item)
    return ret


@router.put(
    "",
    response_model=Telegram,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Result},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Result},
        status.HTTP_409_CONFLICT: {"model": Result},
    },
)
async def put_telegram(
    item: Telegram, user: Optional[UserInDB] = Depends(get_actual_user)
):
    if item.id is None:
        return get_error(
            key=KEYS_ERROR.id_not_found, status_code=status.HTTP_400_BAD_REQUEST
        )
    if hasattr(item, "username_insert"):
        delattr(item, "username_insert")
    if hasattr(item, "username_update"):
        delattr(item, "username_update")
    item.username_update = user.username
    # Verify exist segment name
    segment = Segment(name=item.segment)
    segments = segment_service.getByName(segment)
    if segments == []:
        return get_error(
            key=KEYS_ERROR.segment_not_found, status_code=status.HTTP_409_CONFLICT
        )
    ret = telegram_service.update(item)
    if ret is None:
        return get_error(
            key=KEYS_ERROR.object_not_found, status_code=status.HTTP_404_NOT_FOUND
        )
    print(ret)
    ret = telegram_service.getByID(item)
    return ret


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Result},
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": Result},
    },
)
async def delete_telegram(
    id: PyObjectId, user: Optional[UserInDB] = Depends(get_actual_user)
):
    item = Telegram(name="", chat_id="", segment="")
    item.username_update = user.username
    item.id = id
    if item.id is None:
        return get_error(
            key=KEYS_ERROR.id_not_found, status_code=status.HTTP_400_BAD_REQUEST
        )

    ret = telegram_service.getByID(item)
    if ret is None:
        return get_error(
            key=KEYS_ERROR.object_not_found, status_code=status.HTTP_404_NOT_FOUND
        )

    ret = telegram_service.delete(item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
