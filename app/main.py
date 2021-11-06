import time
from typing import Optional

from starlette.requests import Request
from app.access import get_actual_user
from fastapi.params import Depends
from starlette.responses import JSONResponse
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import uvicorn

from app.core import configuration
from app.routers import users, oauth_google
from app.routers import slack
from app.routers import token
from app.routers import whatsapp
from app.routers import telegram
from app.routers import discord
from app.routers import phone
from app.routers import segment
from app.routers import notify
from app.routers import history

from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, BackgroundTasks

TITLE = configuration.APP_TITLE
DESCRIPTION = configuration.APP_DESCRIPTION
VERSION = configuration.APP_VERSION
app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=VERSION,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)


@app.get("/api/", tags=["Index"])
def read_root():
    return {"title": TITLE, "description": DESCRIPTION, "version": VERSION}


app.add_middleware(
    SessionMiddleware, secret_key=configuration.APP_SECRET_KEY_MIDDLEWARE
)
app.include_router(oauth_google.router, prefix="/api/google", tags=["Security Google"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(segment.router, prefix="/api/segment", tags=["Segment"])
app.include_router(token.router, prefix="/api/token", tags=["Token"])
app.include_router(slack.router, prefix="/api/slack", tags=["Slack"])
app.include_router(whatsapp.router, prefix="/api/whatsapp", tags=["WhatsApp"])
app.include_router(telegram.router, prefix="/api/telegram", tags=["Telegram"])
app.include_router(discord.router, prefix="/api/discord", tags=["Discord"])
app.include_router(phone.router, prefix="/api/phone", tags=["Phone"])
app.include_router(notify.router, prefix="/api/notify", tags=["Notify"])
app.include_router(history.router, prefix="/api/history", tags=["History"])


@app.get("/api/docs", tags=["Documentation"])  # Tag it as "documentation" for our docs
async def get_documentation(
    request: Request, user: Optional[dict] = Depends(get_actual_user)
):  # This dependency protects our endpoint!
    response = get_swagger_ui_html(
        openapi_url="/api/openapi.json", title="Documentation"
    )
    return response


@app.get("/api/openapi.json", tags=["Documentation"])
async def get_open_api_endpoint(
    request: Request, user: Optional[dict] = Depends(get_actual_user)
):  # This dependency protects our endpoint!
    response = JSONResponse(
        get_openapi(title=TITLE, version=VERSION, routes=app.routes)
    )
    return response


@app.get("/api/redoc", tags=["Documentation"])  # Tag it as "documentation" for our docs
async def redoc_html(
    request: Request, user: Optional[dict] = Depends(get_actual_user)
):  # This dependency protects our endpoint!
    response = get_redoc_html(openapi_url="/api/openapi.json", title="Documentation")
    return response
