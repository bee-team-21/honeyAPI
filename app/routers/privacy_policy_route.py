import os
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter()
dirpath = os.path.dirname(__file__)
path = os.path.join(dirpath, "..", "templates")
templates = Jinja2Templates(directory=path)
@router.get("")
async def get_privacy_policy(request: Request):
    return templates.TemplateResponse("policy.html",{"request": request})