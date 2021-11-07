from typing import List, Literal, Optional
from urllib.parse import urlunsplit
from fastapi.openapi.models import APIKey
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse, Response
from fastapi import APIRouter, Depends, status
from app.backgroud.risk_notify import write_segments_risk
from app.models.risk_model import Risk

from app.models.user import UserInDB
from app.models.user_report_model import UserReportBot, UserReportResponse
from app.models.result import Result
from app.access import get_actual_user, get_api_key
from app.services import segment_service, sites_service
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
    background_tasks: BackgroundTasks,
    user: APIKey = Depends(get_api_key)
):
    file, content_type, filename, extension = downloader_file(report.image)
    print (content_type, filename, extension)
    url = blobstorage.upload(data=file,extension=extension)
    if url is not None:
        #TODO send to recognition return risk
        print (url)
        risk = Risk(risk='low',confidence=0.8, detail="Test Case")
        risk.image = url
        risk.imageBinary = file 
        risk.imageContentType = content_type
        risk.imageFilename = filename



        segments = segment_service.getByRisk(risk.risk)
        if segments != []:
            background_tasks.add_task(write_segments_risk, risk=risk,segments=segments,user=user.get("username"))
        
        return UserReportResponse(detail=risk.risk +" > "+ risk.detail) #TODO

    else:
        return UserReportResponse(detail=get_error_message(key=KEYS_ERROR.cant_upload_blob).message) #TODO
    