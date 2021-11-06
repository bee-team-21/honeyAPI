from typing import Union
import telegram
from app.core import configuration

TOKEN = configuration.APP_TELEGRAM_TOKEN
# token that can be generated talking with @BotFather on telegram
# To view groups  use https://api.telegram.org/botXXXXXX:YYYYYYYYYYYY/getUpdates


def sendText(msg: str, chat_id: str):
    bot = telegram.Bot(token=TOKEN)
    result = bot.sendMessage(chat_id=chat_id, text=msg)
    return result


def sendImage(chat_id: str, caption: str, photo: Union[bytes, str]):
    bot = telegram.Bot(token=TOKEN)
    result = bot.send_photo(chat_id=chat_id, caption=caption, photo=photo)
    return result


# sendText("Hola","-")
# sendImage(chat_id="-411724843", caption="Test", photo=open('10110257.jpg', 'rb'))
