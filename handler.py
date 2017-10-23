import requests
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import ImageMessage
from linebot.models import MessageEvent
from linebot.models import TextMessage

from settings import CHANNEL_SECRET, CHANNEL_TOKEN

line_bot_api = LineBotApi(CHANNEL_TOKEN)
event_handler = WebhookHandler(CHANNEL_SECRET)


@event_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    data = {
        "USERID": event.source.user_id,
        "MESSAGE": event.message.text,
        "TOKENID": event.reply_token
    }
    requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/ASKBOBV2",json=data)


@event_handler.add(MessageEvent,message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    content = message_content.content
    headers = {'Content-type': message_content.content_type}
    requests.post('https://line-chatbot-kos.herokuapp.com/test', headers=headers, files={'image': content})