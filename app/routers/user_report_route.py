from typing import List, Literal, Optional
from urllib.parse import urlunsplit
from fastapi.openapi.models import APIKey
from starlette.responses import JSONResponse, Response
from fastapi import APIRouter, Depends, status

from app.models.user import UserInDB
from app.models.user_report_model import UserReportBot, UserReportResponse
from app.models.result import Result
from app.access import get_actual_user, get_api_key
from app.services import sites_service
from app.utils import blobstorage
from app.utils.downloadImage import downloader_file
from app.validators.mongo import PyObjectId
from app.utils.responses import KEYS_ERROR, get_error_message
from app.utils.result import get_error
import urllib.request
router = APIRouter()

    
@router.post("", response_model=UserReportResponse, status_code=status.HTTP_200_OK)
async def search_sites_external(
    report: UserReportBot,
    user: APIKey = Depends(get_api_key)
):
    file, content_type, filename, extension = downloader_file(report.image)
    url = blobstorage.upload(data=file,extension=extension)
    if url is not None:
        #TODO send to recognition
        print (url)
        return UserReportResponse(detail="Su imagen fue procesada con: "+url) #TODO
    else:
        return UserReportResponse(detail=get_error_message(key=KEYS_ERROR.cant_upload_blob).message) #TODO
    