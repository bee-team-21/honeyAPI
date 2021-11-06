from typing import List, Literal, Optional
from starlette.responses import JSONResponse, Response
from fastapi import APIRouter, Depends, status

from app.models.user import UserInDB
from app.models.sites_model import Sites
from app.models.result import Result
from app.access import get_actual_user
from app.services import sites_service
from app.validators.mongo import PyObjectId
from app.utils.responses import KEYS_ERROR
from app.utils.result import get_error

router = APIRouter()


@router.get("", response_model=List[Sites], status_code=status.HTTP_200_OK)
async def get_sites(
    user: Optional[UserInDB] = Depends(get_actual_user), q: Optional[str] = None,
    type: Literal['M', 'F', 'Z'] = 'M'
):
    search = Sites(name="", type=type)
    if q is not None:
        search.name = q
        items = sites_service.search(item=search)
    else:
        items = sites_service.get()
    return items


@router.post("", response_model=Sites, status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": Sites},
        status.HTTP_409_CONFLICT: {"model": Result},
    }
)
async def post_sites(item: Sites, user: Optional[UserInDB] = Depends(get_actual_user)):
    item.username_insert=user.username
    alreadyExist = sites_service.getByName(item=item)
    if alreadyExist != []:
        return get_error(key=KEYS_ERROR.name_already_exist, status_code=status.HTTP_409_CONFLICT)
    ret = sites_service.create(item)
    item.id = ret.inserted_id
    ret = sites_service.getByID(item)
    return ret


@router.put(
    "",
    response_model=Sites,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": Result},
        status.HTTP_404_NOT_FOUND: {"model": Result},
        status.HTTP_409_CONFLICT: {"model": Result},
    },
)
async def put_sites(item: Sites, user: Optional[UserInDB] = Depends(get_actual_user)):
    if item.id is None:
        return get_error(key=KEYS_ERROR.id_not_found, status_code=status.HTTP_400_BAD_REQUEST)
    
    oldItem = sites_service.getByID(item)
    if oldItem is None:
        return get_error(key=KEYS_ERROR.object_not_found, status_code=status.HTTP_404_NOT_FOUND)

    alreadyExist = sites_service.getByNameAndNotID(item=item)
    if alreadyExist != []:
        return get_error(key=KEYS_ERROR.name_already_exist, status_code=status.HTTP_409_CONFLICT)

    item.username_update=user.username
    ret = sites_service.update(item)
    ret = sites_service.getByID(item)
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
    item = Sites(name="")
    item.id = id
    if item.id is None:
        return get_error(key=KEYS_ERROR.id_not_found, status_code=status.HTTP_400_BAD_REQUEST)
    ret = sites_service.getByID(item)
    if ret is None:
        return get_error(key=KEYS_ERROR.object_not_found, status_code=status.HTTP_404_NOT_FOUND)
        
    item.username_update=user.username
    ret = sites_service.delete(item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
