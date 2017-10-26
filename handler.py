import json

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

from helper import create_message, create_messages
from settings import CHANNEL_SECRET, CHANNEL_TOKEN

line_bot_api = LineBotApi(CHANNEL_TOKEN)
event_handler = WebhookHandler(CHANNEL_SECRET)


@event_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    json_data = {
        "USERID": event.source.user_id,
        "MESSAGE": event.message.text,
        "TOKENID": event.reply_token
    }
    r = requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/ASKBOBV2",json=json_data, timeout=20)
    data = r.json()['STATUS'][0]
    print(data)
    data = json.dumps(data['messages'])
    print(data)
    messages = create_messages(data['messages'])
    print(messages)
    line_bot_api.reply_message(event.reply_token, messages)



@event_handler.add(MessageEvent,message=[ImageMessage])
def handle_image_message(event):
    param = "?USERID="+event.source.user_id+"&TOKENID="+event.reply_token
    message_content = line_bot_api.get_message_content(event.message.id)
    content = message_content.content
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    try:
        r = requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/POSTIMAGEV2"+param, headers=headers, data=content, timeout=20)
        data = r.json()['STATUS'][0]
        messages = create_messages(data['messages'])
        line_bot_api.reply_message(event.reply_token, messages)
    except Exception as e:
        print("Yellow Monkey Error")
        print(e)
        line_bot_api.push_message(event.source.user_id, [TextSendMessage(text=str(e))])


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
        r = requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/ASKBOBV2_LOCATION",json=json, timeout=20)
        data = r.json()['STATUS'][0]
        messages = create_messages(data['messages'])
        line_bot_api.reply_message(event.reply_token, messages)
    except Exception as e:
        print("Blue Monkey Error")
        print(e)
        line_bot_api.push_message(event.source.user_id,[TextSendMessage(text=str(e))])

