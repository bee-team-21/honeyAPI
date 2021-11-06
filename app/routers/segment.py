from typing import List, Optional
from starlette.responses import JSONResponse, Response
from fastapi import APIRouter, Depends, status

from app.models.user import UserInDB
from app.models.segment import Segment
from app.models.result import Result
from app.access import get_actual_user
from app.services import segment_service, slack_service, whatsapp_service, phone_service
from app.validators.mongo import PyObjectId
from app.utils.responses import KEYS_ERROR
from app.utils.result import get_error

router = APIRouter()


@router.get("", response_model=List[Segment], status_code=status.HTTP_200_OK)
async def get_segment(
    user: Optional[UserInDB] = Depends(get_actual_user), q: Optional[str] = None
):
    search = Segment(name="")
    if q is not None:
        search.name = q
        items = segment_service.search(item=search)
    else:
        items = segment_service.get()
    return items


@router.post("", response_model=Segment, status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": Segment},
        status.HTTP_409_CONFLICT: {"model": Result},
    }
)
async def post_segment(item: Segment, user: Optional[UserInDB] = Depends(get_actual_user)):
    item.username_insert=user.username
    alreadyExist = segment_service.getByName(item=item)
    if alreadyExist != []:
        return get_error(key=KEYS_ERROR.name_already_exist, status_code=status.HTTP_409_CONFLICT)
    ret = segment_service.create(item)
    item.id = ret.inserted_id
    ret = segment_service.getByID(item)
    return ret


@router.put(
    "",
    response_model=Segment,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Result},
        status.HTTP_404_NOT_FOUND: {"model": Result},
        status.HTTP_409_CONFLICT: {"model": Result},
    },
)
async def put_segment(item: Segment, user: Optional[UserInDB] = Depends(get_actual_user)):
    if item.id is None:
        return get_error(key=KEYS_ERROR.id_not_found, status_code=status.HTTP_400_BAD_REQUEST)
    
    oldItem = segment_service.getByID(item)
    if oldItem is None:
        return get_error(key=KEYS_ERROR.object_not_found, status_code=status.HTTP_404_NOT_FOUND)

    alreadyExist = segment_service.getByNameAndNotID(item=item)
    if alreadyExist != []:
        return get_error(key=KEYS_ERROR.name_already_exist, status_code=status.HTTP_409_CONFLICT)

    item.username_update=user.username
    ret = segment_service.update(item)
    ret = segment_service.getByID(item)
    #Update segment name in all SLACK, WP, PHONE
    res_slack = slack_service.update_segment(oldsegment=oldItem.name ,newsegment=ret.name)
    res_whatsapp = whatsapp_service.update_segment(oldsegment=oldItem.name ,newsegment=ret.name)
    res_phone = phone_service.update_segment(oldsegment=oldItem.name ,newsegment=ret.name)
    print ("#"*30)
    print (res_slack,res_whatsapp,res_phone)
    print ("#"*30)
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
async def delete_segment(
    id: PyObjectId, user: Optional[UserInDB] = Depends(get_actual_user)
):
    item = Segment(name="")
    item.id = id
    if item.id is None:
        return get_error(key=KEYS_ERROR.id_not_found, status_code=status.HTTP_400_BAD_REQUEST)
    ret = segment_service.getByID(item)
    if ret is None:
        return get_error(key=KEYS_ERROR.object_not_found, status_code=status.HTTP_404_NOT_FOUND)
        
    item.username_update=user.username
    ret = segment_service.delete(item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
