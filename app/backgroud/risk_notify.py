
from typing import List
from app.models.discord import Discord
from app.models.history import History, Plataform
from app.models.risk_model import Risk
from app.models.segment import Segment
from app.services import discord_service, history_service
from app.utils import discord_webhook
from app.utils.downloadImage import downloader_file
from app.utils.riskText import riskColor
def write_segments_risk(risk: Risk, segments: List[Segment], user: str):
    #Obtain Discord Webhooks
    item_discord = []
    for i_segment in segments:
        item_discord.extend(
            discord_service.get_by_segment(
                Discord(segment=i_segment.name, name="", channel_webhook="")
            )
        )
    if item_discord != []:
        #Prepare notification
        initResponse = riskColor(risk.risk)
        text='{} {} Reporte en: {}. '.format(initResponse,risk.detail,risk.site)
        # text_en = '{} {} Report from: {}. '.format(initResponse,risk.detail,risk.site)
        finalMessage= text + risk.gps
        for discord in item_discord:
            response = discord_webhook.send_message(discord.channel_webhook, finalMessage,risk.imageBinary, risk.imageContentType, risk.imageFilename)
            log = History()
            log.username_insert = user
            log.plataform = Plataform.discord
            log.request_payload = text
            log.response_code = response.status_code
            log.response_text = response.text
            log.image = risk.image
            log.activator = write_segments_risk.__name__
            history_service.create(log)