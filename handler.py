import requests
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import AudioMessage
from linebot.models import ImageMessage
from linebot.models import MessageEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage
from linebot.models import VideoMessage
from linebot.models import LocationMessage
from urllib3.exceptions import MaxRetryError

from settings import CHANNEL_SECRET, CHANNEL_TOKEN

line_bot_api = LineBotApi(CHANNEL_TOKEN)
event_handler = WebhookHandler(CHANNEL_SECRET)


@event_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    json = {
        "USERID": event.source.user_id,
        "MESSAGE": event.message.text,
        "TOKENID": event.reply_token
    }
    try:
        requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/ASKBOBV2",json=json, timeout=20)
    except MaxRetryError:
        line_bot_api.push_message(event.source.user_id,[TextSendMessage(text='Error getting data from inventech, please retry')])


@event_handler.add(MessageEvent,message=[ImageMessage])
def handle_image_message(event):
    json = {
        "USERID": event.source.user_id,
        "TOKENID": event.reply_token
    }
    message_content = line_bot_api.get_message_content(event.message.id)
    content = message_content.content
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    try:
        requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/POSTIMAGE", headers=headers, json=json, data=content, timeout=20)
    except MaxRetryError:
        line_bot_api.push_message(event.source.user_id,[TextSendMessage(text='Error getting data from inventech, please retry')])


@event_handler.add(MessageEvent,message=[LocationMessage])
def handle_location_message(event):
    json = {
        "USERID": event.source.user_id,
        "TOKENID": event.reply_token,
        "title":event.message.title,
        "address":event.message.address,
        "latitude":event.message.latitude,
        "longitude":event.message.longitude,
    }
    try:
        requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/ASKBOBV2_LOCATION",json=data, timeout=20)
    except:
        line_bot_api.push_message(event.source.user_id,[TextSendMessage(text='Error getting data from inventech, please retry')])