import traceback
from typing import List, Optional
from app.models.discord import Discord, DiscordMessage, DiscordNotify
from app.models.user import UserInDB
from app.utils import discord_webhook, telegram_bot_api
from app.models.telegram import (
    Telegram,
    TelegramNotify,
    TelegramNotifyText,
)
from app.models.whatsapp import (
    WhatsApp,
    WhatsAppNotify,
    WhatsAppNotifyText,
)
import json
from fastapi.openapi.models import APIKey
from fastapi import status, Response
from fastapi import APIRouter, Depends, BackgroundTasks


from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.core import configuration
from app.access import get_actual_user, get_api_key
from app.models.forbidden import Forbidden
from app.models.notify import Notify, switch
from app.models.result import Result
from app.models.segment import Segment
from app.models.slack import Slack
from app.models.history import History, Plataform
from app.models.File import File

from app.utils import whatsapp_chat_api
from app.utils.downloadImage import downloader_file
from app.utils.responses import KEYS_SUCCESS, KEYS_ERROR
from app.validators.mongo import PyObjectId

# from app.models.prometheus import Alertmanager
from app.services import (
    discord_service,
    file_service,
    segment_service,
    slack_service,
    history_service,
    whatsapp_service,
    telegram_service,
)
from app.utils.result import get_error, get_success
# from app.backgroud.notify import write_notification_prometheus
router = APIRouter()


SAVE_IMAGES = configuration.APP_ENABLE_SAVE_IMAGES
if SAVE_IMAGES == True:

    @router.get(
        "/files",
        response_model=List[File], status_code=status.HTTP_200_OK
    )
    async def get_files_saved_id(user: Optional[UserInDB] = Depends(get_actual_user), q: Optional[str] = None):
        if q is not None:
            item = File(image=None, filename=None, mimetype=None)
            item.filename = q
            item.mimetype = q
            items = file_service.search(item=item)
        else:
            items = file_service.get()
        return items

    @router.get(
        "/files/{id}",
        responses={
            status.HTTP_200_OK: {"content": {"image/png": {}}},
            status.HTTP_404_NOT_FOUND: {"model": Result},
        },
    )
    async def get_files_saved(id: PyObjectId, response: Response):
        item = File(image=None, filename=None, mimetype=None)
        item.id = id
        finded = file_service.getByID(item=item)
        if finded is None:
            return get_error(
                key=KEYS_ERROR.object_not_found, status_code=status.HTTP_404_NOT_FOUND
            )
        return Response(content=finded.file, media_type=finded.mimetype)

@router.post(
    "/slack/generic",
    responses={
        status.HTTP_403_FORBIDDEN: {"model": Forbidden},
        status.HTTP_404_NOT_FOUND: {"model": Result},
    },
)
async def post_generic_notify(item: Notify, user: APIKey = Depends(get_api_key)):
    segment = Segment(name=item.segment)
    segments = segment_service.getByName(segment)
    if segments == []:
        return get_error(
            key=KEYS_ERROR.segment_not_found, status_code=status.HTTP_404_NOT_FOUND
        )

    slackAlert = []
    for iBlock in item.data:
        value = switch(iBlock)
        slackAlert.append(value)

    # For notificar canales
    for i_segment in segments:
        items = slack_service.get_by_segment(
            Slack(segment=i_segment.name, token="", channel="")
        )
        for slack in items:
            client = WebClient(token=slack.token)
            try:
                response = client.chat_postMessage(
                    channel=slack.channel, blocks=slackAlert
                )

                datapayload = json.dumps(slackAlert)
                log = History()
                log.username_insert = user.get("username")
                log.plataform = Plataform.slack
                log.request_payload = datapayload
                log.response_code = response.status_code
                log.response_text = str(response["message"])
                log.activator = post_generic_notify.__name__
                history_service.create(log)
            except SlackApiError as e:
                assert e.response["ok"] is False
                assert e.response[
                    "error"
                ]  # str like 'invalid_auth', 'channel_not_found'
                print(f"Got an error: {e.response['error']}")

                datapayload = json.dumps(slackAlert)
                log = History()
                log.username_insert = user.get("username")
                log.plataform = Plataform.slack
                log.request_payload = datapayload
                log.response_code = 400
                log.response_text = str(e.response["error"])
                log.activator = post_generic_notify.__name__
                history_service.create(log)

    return slackAlert


# @router.post(
#     "/prometheus",
#     response_model=Result,
#     responses={
#         status.HTTP_403_FORBIDDEN: {"model": Forbidden},
#         status.HTTP_404_NOT_FOUND: {"model": Result},
#     },
# )
# async def post_prometheus(item: Alertmanager,  background_tasks: BackgroundTasks, user: APIKey = Depends(get_api_key)):
#     print(".-.-.-.-.-.-.-.-.-.-.-.",item)
#     segment = Segment(name=item.receiver)
#     print(".-.-.-.-.-.-.-.-.-.-.-.name=item.receiver:", item.receiver)
#     segments = segment_service.getByName(segment)
#     if segments == []:
#         return get_error(
#             key=KEYS_ERROR.segment_not_found, status_code=status.HTTP_404_NOT_FOUND
#         )
#     background_tasks.add_task(write_notification_prometheus, item=item,segments=segments, user=user.get("username")) 
#     return get_success(
#             key=KEYS_SUCCESS.notify_in_backgroud, status_code=status.HTTP_200_OK
#         )




@router.post(
    "/whatsapp/generic",
    responses={
        status.HTTP_403_FORBIDDEN: {"model": Forbidden},
        status.HTTP_404_NOT_FOUND: {"model": Result},
    },
)
async def post_generic_whatsapp(
    item: WhatsAppNotify, user: APIKey = Depends(get_api_key)
):
    segment = Segment(name=item.segment)
    segments = segment_service.getByName(segment)
    if segments == []:
        return get_error(
            key=KEYS_ERROR.segment_not_found, status_code=status.HTTP_404_NOT_FOUND
        )
    for i_segment in segments:
        # Notify WP
        items = whatsapp_service.get_by_segment(
            WhatsApp(segment=i_segment.name, name="", group_id="")
        )
        if items != []:
            for wp in items:
                for message in item.messages:
                    text = ""
                    if type(message) == type(WhatsAppNotifyText(text="")):
                        text = message.text
                        response = whatsapp_chat_api.sendText(
                            chatID=wp.group_id, message=message.text
                        )
                    else:
                        text = message.caption
                        response = whatsapp_chat_api.sendFileURL(
                            chatID=wp.group_id,
                            filePublicURL=message.url,
                            caption=message.caption,
                            fileName=message.filename,
                        )
                        log = History()
                        log.username_insert = user.get("username")
                        log.plataform = Plataform.whatsapp
                        log.request_payload = text
                        log.response_code = response.status_code
                        log.response_text = response.text
                        log.activator = post_generic_whatsapp.__name__
                        history_service.create(log)
    return item


@router.post(
    "/telegram/generic",
    responses={
        status.HTTP_403_FORBIDDEN: {"model": Forbidden},
        status.HTTP_404_NOT_FOUND: {"model": Result},
    },
)
async def post_generic_telegram(
    item: TelegramNotify, user: APIKey = Depends(get_api_key)
):
    segment = Segment(name=item.segment)
    segments = segment_service.getByName(segment)
    if segments == []:
        return get_error(
            key=KEYS_ERROR.segment_not_found, status_code=status.HTTP_404_NOT_FOUND
        )
    for i_segment in segments:
        # Notify WP
        items = telegram_service.get_by_segment(
            Telegram(segment=i_segment.name, name="", chat_id="")
        )
        if items != []:
            for tele in items:
                for message in item.messages:
                    text = ""
                    if type(message) == type(TelegramNotifyText(text="")):
                        text = message.text
                        response = telegram_bot_api.sendText(
                            chat_id=tele.chat_id, msg=message.text
                        )
                    else:
                        text = message.caption
                        response = telegram_bot_api.sendImage(
                            chat_id=tele.chat_id,
                            photo=message.url,
                            caption=message.caption,
                        )
                        log = History()
                        log.username_insert = user.get("username")
                        log.plataform = Plataform.telegram
                        log.request_payload = text
                        log.response_code = 200
                        log.response_text = str(response)
                        log.activator = post_generic_telegram.__name__
                        history_service.create(log)
    return item



@router.post(
    "/discord/generic",
    responses={
        status.HTTP_403_FORBIDDEN: {"model": Forbidden},
        status.HTTP_404_NOT_FOUND: {"model": Result},
    },
)
async def post_generic_discord(
    item: DiscordNotify, user: APIKey = Depends(get_api_key)
):
    segment = Segment(name=item.segment)
    segments = segment_service.getByName(segment)
    if segments == []:
        return get_error(
            key=KEYS_ERROR.segment_not_found, status_code=status.HTTP_404_NOT_FOUND
        )
    for i_segment in segments:
        items = discord_service.get_by_segment(
            Discord(segment=i_segment.name, name="", channel_webhook="")
        )
        if items != []:
            for message in item.messages:
                text = message.text
                data_file = None
                #download images
                if  message.file is not None:
                    file, content_type, filename = downloader_file(message.file.url, header=message.file.header, header_content=message.file.header_content)
                    data_file = file
                    if SAVE_IMAGES == True:
                        file_service.create(File(file=file, mimetype=content_type, filename=filename ))  # Save Images on Mongo
                for discord in items:
                    if data_file is not None:
                        response = discord_webhook.send_message(discord.channel_webhook, text,data_file, content_type, filename)
                    else:
                        response = discord_webhook.send_message(discord.channel_webhook, text)
                log = History()
                log.username_insert = user.get("username")
                log.plataform = Plataform.discord
                log.request_payload = text
                log.response_code = response.status_code
                log.response_text = response.text
                log.activator = post_generic_discord.__name__
                history_service.create(log)
    return item