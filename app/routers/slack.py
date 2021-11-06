from typing import List, Optional
from starlette.responses import Response
from fastapi import APIRouter, Depends, status

from app.models.segment import Segment
from app.models.user import UserInDB
from app.models.slack import Slack
from app.models.result import Result
from app.access import get_actual_user
from app.services import slack_service, segment_service
from app.validators.mongo import PyObjectId
from app.utils.result import get_error
from app.utils.responses import KEYS_ERROR

router = APIRouter()


@router.get("", response_model=List[Slack], status_code=status.HTTP_200_OK)
async def get_slack(
    user: Optional[UserInDB] = Depends(get_actual_user), q: Optional[str] = None
):
    search = Slack(token="", channel="", segment="")
    if q is not None:
        search.token = q
        search.name = q
        slacks = slack_service.search(slack=search)
    else:
        slacks = slack_service.get()
    return slacks


@router.post("", response_model=Slack, status_code=status.HTTP_201_CREATED
    ,responses={
        status.HTTP_201_CREATED: {"model": Slack},
        status.HTTP_409_CONFLICT: {"model": Result},
    }
)
async def post_slack(item: Slack, user: Optional[UserInDB] = Depends(get_actual_user)):
    item.username_insert=user.username
    # Verify exist segment name
    segment = Segment(name=item.segment)
    segments = segment_service.getByName(segment)
    if segments == []:
        return get_error(key=KEYS_ERROR.segment_not_found, status_code=status.HTTP_409_CONFLICT)
    ret = slack_service.create(item)
    item.id = ret.inserted_id
    ret = slack_service.get_by_ID(item)
    return ret


@router.put(
    "",
    response_model=Slack,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Result},
        status.HTTP_404_NOT_FOUND: {"model": Result},
        status.HTTP_409_CONFLICT: {"model": Result},
    },
)
async def put_slack(item: Slack, user: Optional[UserInDB] = Depends(get_actual_user)):
    if item.id is None:
        return get_error(key=KEYS_ERROR.id_not_found, status_code=status.HTTP_400_BAD_REQUEST)
    item.username_update=user.username
    # Verify exist segment name
    segment = Segment(name=item.segment)
    segments = segment_service.getByName(segment)
    if segments == []:
        return get_error(key=KEYS_ERROR.segment_not_found, status_code=status.HTTP_409_CONFLICT)

    ret = slack_service.update(item)
    if ret is None:
        return get_error(key=KEYS_ERROR.object_not_found, status_code=status.HTTP_404_NOT_FOUND)
    ret = slack_service.get_by_ID(item)
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
async def delete_slack(
    id: PyObjectId, user: Optional[UserInDB] = Depends(get_actual_user)
):
    item = Slack(token="", channel="", segment="")
    item.id = id
    if item.id is None:
        return get_error(key=KEYS_ERROR.id_not_found, status_code=status.HTTP_400_BAD_REQUEST)
    ret = slack_service.get_by_ID(item)
    if ret is None:
        return get_error(key=KEYS_ERROR.object_not_found, status_code=status.HTTP_404_NOT_FOUND)
        
    item.username_update=user.username
    ret = slack_service.delete(item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
