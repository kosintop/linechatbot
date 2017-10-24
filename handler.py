import requests
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import AudioMessage
from linebot.models import ImageMessage
from linebot.models import MessageEvent
from linebot.models import TextMessage
from linebot.models import VideoMessage
from linebot.models import LocationMessage

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
    requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/ASKBOBV2",json=data, timeout=20)


@event_handler.add(MessageEvent,message=[ImageMessage])
def handle_image_message(event):
    print(event.message.id)
    message_content = line_bot_api.get_message_content(event.message.id)
    content = message_content.content
    
    try:
        import sys
        import binascii
        jpeg_signatures = [
            binascii.unhexlify(b'FFD8FFD8'),
            binascii.unhexlify(b'FFD8FFE0'),
            binascii.unhexlify(b'FFD8FFE1')
        ]
        first_four_bytes = content.read(4)
        if first_four_bytes in jpeg_signatures:
            print("JPEG detected.")
         else:
            print("File does not look like a JPEG.")
    except:
        print("exception")
        pass
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/POSTIMAGE", headers=headers, files={'file': ('test.jpg',content,'application/octet-stream')}, timeout=20)


@event_handler.add(MessageEvent,message=[LocationMessage])
def handle_location_message(event):
    data = {
        "USERID": event.source.user_id,
        "TOKENID": event.reply_token,
		"title":event.message.title,
		"address":event.message.address,
		"latitude":event.message.latitude,
		"longitude":event.message.longitude,
    }
    r = requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/ASKBOBV2_LOCATION",json=data, timeout=20)
    print(data)
    print(r.content)