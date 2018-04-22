import json

import requests
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models import ImageMessage
from linebot.models import MessageEvent
from linebot.models import PostbackEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage
from linebot.models import LocationMessage
from requests.adapters import HTTPAdapter

from helper import create_messages, create_imagemap
from settings import CHANNEL_SECRET, CHANNEL_TOKEN,API_URL

line_bot_api = LineBotApi(CHANNEL_TOKEN)
event_handler = WebhookHandler(CHANNEL_SECRET)


def reply_message(messages,user_id,token_id):
    try:
        line_bot_api.reply_message(token_id, messages)
    except LineBotApiError as e:
        print('LineBotApiError')
        print(e.status_code)
        try:
            print('unable to reply, trying push instead')
            line_bot_api.push_message(user_id,messages)
        except Exception as e:
            print('Unable to reply and push')
            print(e)


def send_data_to_inventech(endpoint,headers=None,json_data=None,binary_data=None):
    print(json_data)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    print(API_URL+endpoint)
    # sending data to inventech
    try:
        r = s.post(API_URL+endpoint,
                   headers=headers,
                   json=json_data,
                   data=binary_data,
                   timeout=60
                   )
    except Exception as e:
        print('error process request to server')
        print(e)
        json_messages = [
            {'type':'text','text':'Cannot process request, please try again'}
        ]
        messages = create_messages(json_messages)
        reply_message(messages,json_data['USERID'],json_data['TOKENID'])
        return

    if r.status_code == 200:
        print('successfully get server response')
        print(r.json())

        data = r.json()['STATUS'][0]
        json_messages = json.loads(data['messages'])

        messages = create_messages(json_messages)
        reply_message(messages, json_data['USERID'], json_data['TOKENID'])

    else:
        print('fail to get server response', r.status_code)
        json_messages = [
            {'type':'text','text':'Cannot connect to server, please try again'}
        ]
        messages = create_messages(json_messages)
        reply_message(messages, json_data['USERID'], json_data['TOKENID'])


@event_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    json_data = {
        "USERID": event.source.user_id,
        "MESSAGE": event.message.text,
        "TOKENID": event.reply_token
    }

    if event.message.text == 'imagemap':
        message = create_imagemap()
        line_bot_api.push_message(event.source.user_id, [message])
        return

    try:
        send_data_to_inventech('/ASKBOBV2',json_data=json_data)
    except Exception as e:
        print("Red Monkey Error")
        print(e)
        line_bot_api.push_message(event.source.user_id, [TextSendMessage(text=str(e))])


@event_handler.add(MessageEvent,message=[ImageMessage])
def handle_image_message(event):
    json_data = {
        "USERID": event.source.user_id,
        "TOKENID": event.reply_token
    }
    param = "?USERID="+event.source.user_id+"&TOKENID="+event.reply_token
    message_content = line_bot_api.get_message_content(event.message.id)
    content = message_content.content
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    try:
        send_data_to_inventech('/POSTIMAGEV2'+param, json_data=json_data, binary_data=content,headers=headers)
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