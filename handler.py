import json

import requests
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import ImageMessage
from linebot.models import MessageEvent
from linebot.models import PostbackEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage
from linebot.models import LocationMessage
from requests.adapters import HTTPAdapter

from helper import create_messages
from settings import CHANNEL_SECRET, CHANNEL_TOKEN,API_URL

line_bot_api = LineBotApi(CHANNEL_TOKEN)
event_handler = WebhookHandler(CHANNEL_SECRET)


def send_data_to_inventech(endpoint,headers=None,json_data=None,binary_data=None):
    print(json_data)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    r = s.post(API_URL+endpoint,
               headers=headers,
               json=json_data,
               data=binary_data,
               timeout=60
               )


    print(r.status_code)
    print(r.json())

    if r.status_code == 200:
        print('successfully get server response')
        data = r.json()['STATUS'][0]
        json_messages = json.loads(data['messages'])

        messages = create_messages(json_messages)
        line_bot_api.reply_message(data['replytoken'], messages)
    else:
        print('fail to get server response')
        json_messages = [
            {'type':'text','text':'Cannot connect to server, please try again'}
        ]
        messages = create_messages(json_messages)
        line_bot_api.reply_message(json_data['TOKENID'], messages)


@event_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    json_data = {
        "USERID": event.source.user_id,
        "MESSAGE": event.message.text,
        "TOKENID": event.reply_token
    }

    try:
        send_data_to_inventech('/ASKBOBV2',json_data=json_data)
    except Exception as e:
        print("Red Monkey Error")
        print(e)
        line_bot_api.push_message(event.source.user_id, [TextSendMessage(text=str(e))])


@event_handler.add(MessageEvent,message=[ImageMessage])
def handle_image_message(event):
    param = "?USERID="+event.source.user_id+"&TOKENID="+event.reply_token
    message_content = line_bot_api.get_message_content(event.message.id)
    content = message_content.content
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    try:
        send_data_to_inventech('/POSTIMAGEV2'+param, binary_data=content,headers=headers)
    except Exception as e:
        print("Yellow Monkey Error")
        print(e)
        line_bot_api.push_message(event.source.user_id, [TextSendMessage(text=str(e))])


@event_handler.add(MessageEvent,message=[LocationMessage])
def handle_location_message(event):
    json_data = {
        "USERID": event.source.user_id,
        "TOKENID": event.reply_token,
        "title":event.message.title,
        "address":event.message.address,
        "latitude":event.message.latitude,
        "longitude":event.message.longitude,
    }

    try:
        send_data_to_inventech('/ASKBOBV2_LOCATION', json_data=json_data)
    except Exception as e:
        print("Green Monkey Error")
        print(e)
        line_bot_api.push_message(event.source.user_id, [TextSendMessage(text=str(e))])


@event_handler.add(PostbackEvent)
def handle_postback(event):
    print(event)