import requests
import json
import base64
import uuid
from app.core import configuration

INSTANCE = configuration.APP_CHAT_API_INSTANCE
TOKEN = configuration.APP_CHAT_API_TOKEN


def sendText(message: str, chatID: str):
    payload = json.dumps({"body": message, "chatId": chatID})
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(
        url="{0}/sendMessage?token={1}".format(INSTANCE, TOKEN),
        headers=headers,
        data=payload,
    )
    return response


def uidName():
    uid = uuid.uuid4()
    uid = str(uid)
    uid = uid.replace("-", "")
    return uid


def sendFile(
    chatID: str,
    file: bytes,
    caption: str = "",
    fileMimeData: str = "image/jpeg;base64",
    fileName: str = "image.jpg",
):
    encoded_string = base64.b64encode(file)
    payload = json.dumps(
        {
            "body": "data:{0},{1}".format(fileMimeData, encoded_string.decode("utf-8")),
            "filename": "{0}_{1}".format(uidName(), fileName),
            "caption": caption,
            "cached": False,
            "chatId": chatID,
        }
    )
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(
        url="{0}/sendFile?token={1}".format(INSTANCE, TOKEN),
        headers=headers,
        data=payload,
    )
    return response


def sendFileURL(
    chatID: str, filePublicURL: str = "", caption: str = "", fileName: str = "image.jpg"
):
    payload = json.dumps(
        {
            "body": filePublicURL,
            "filename": "{0}_{1}".format(uidName(), fileName),
            "caption": caption,
            "chatId": chatID,
        }
    )
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(
        url="{0}/sendFile?token={1}".format(INSTANCE, TOKEN),
        headers=headers,
        data=payload,
    )
    return response