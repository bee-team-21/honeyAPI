from typing import List, Literal, Optional
from urllib.parse import urlunsplit
from fastapi.openapi.models import APIKey
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse, Response
from fastapi import APIRouter, Depends, status
from app.backgroud.risk_notify import write_segments_risk
from app.core import configuration
from app.models.AnalizysResult_model import AnalysisResult
from app.models.risk_model import Risk
import json
from app.models.sites_model import Sites
from app.models.user import UserInDB
from app.models.user_report_model import UserReport, UserReportBot, UserReportResponse
from app.models.result import Result
from app.access import get_actual_user, get_api_key
from app.services import analysis_service, segment_service, sites_service, user_report_service
from app.utils import blobstorage, facebook_post
from app.utils.downloadImage import downloader_file
from app.utils.riskText import riskColor
from app.validators.mongo import PyObjectId
from app.utils.responses import KEYS_ERROR, get_error_message
from app.utils.result import get_error
import requests
import traceback
import re
router = APIRouter()

    
@router.post("", response_model=UserReportResponse, status_code=status.HTTP_200_OK)
async def search_sites_external(
    report: UserReportBot,
    background_tasks: BackgroundTasks,
    user: APIKey = Depends(get_api_key)
):
    report.site = re.sub(" \((.*?)\)","",report.site)
    sites = sites_service.getByName(Sites(name=report.site, type=""))
    if sites != []:
        site = sites[0].id
    else:
        site = None
    repo = UserReport(
        url=report.image,
        id_site=site
    )
    res = user_report_service.create(repo)
    

    file, content_type, filename, extension = downloader_file(report.image)
    print (content_type, filename, extension)
    url = blobstorage.upload(data=file,extension=extension)
    if url is not None:
        #TODO send to recognition return risk
        risk = Risk(risk='mid',confidence=0.8, detail="")
        risk.image = url
        risk.imageBinary = file 
        risk.imageContentType = content_type
        risk.imageFilename = filename
        if sites != []:
            risk.gps = "https://maps.google.com/maps?q=loc:{},{}".format(sites[0].lat,sites[0].long)
        else:
            risk.gps = ""
        try:
            payload = json.dumps({
            "url": url
            })
            headers = {
            'accept': 'application/json',
            'Authorization': configuration.APP_SERVICE_RECOGNITION_TOKEN
            }
            print(configuration.APP_SERVICE_RECOGNITION_URL)
            response = requests.request("POST", configuration.APP_SERVICE_RECOGNITION_URL, headers=headers, data=payload)
            analysis = json.loads(response.text)
            analysisResult = AnalysisResult(**analysis)
            risk.image = analysisResult.image_url
            risk.detail = analysisResult.text
            risk.site = report.site
            risk.risk = analysisResult.risk[0].grade.lower()

            analysisResult.site = report.site
            analysisResult.site_gps = risk.gps
            analysisResult.id_site = site
            res = analysis_service.create(analysisResult)
        except:
            traceback.print_exc()

        segments = segment_service.getByRisk(risk.risk)
        if segments != []:
            background_tasks.add_task(write_segments_risk, risk=risk,segments=segments,user=user.get("username"))
        initResponse = riskColor(risk.risk)
        detailResponse='{} {} Reporte en: {}. '.format(initResponse,risk.detail,report.site)
        # fb post
        facebook_post.post_image(detailResponse,url)

        # detailResponse_en = '{} {} Report from: {}. '.format(initResponse,risk.detail,report.site)
        finalMessage= detailResponse + risk.gps
        return UserReportResponse(detail=finalMessage)

    else:
        return UserReportResponse(detail=get_error_message(key=KEYS_ERROR.cant_upload_blob).message) #TODO
    