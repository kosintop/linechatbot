import requests
import json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import ImageMessage
from linebot.models import ImageSendMessage
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('oGXtXBuT+Ki0Y1hnL6GfCtiBGZXAMrxhkxpnkqQXRM8BqfNdWAsKUwMUv+/Gqo4nsfgtS0518Tw4YrlR2hucs+Xk+xzmEyCv9QbN31tBQ5dM+Ryc51D9DGpnvF6F7Ogr5+O4qAmZsmIQxnjE3gfpwQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7b7788e4140f7e5252e3bc0da7e0acac')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_profile = get_user_profile(event.source.user_id)
    reply = "Hello " + user_profile.display_name + ", your message was " + event.message.text + ", your user_id is " + user_profile.user_id

    data = {
        "USERID": event.source.user_id,
        "MESSAGE": event.message.text,
        "TOKENID": event.reply_token
    }

    response = requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/ASKBOBV2",json=data)
    print(response.content)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))


@app.route("/push_message", methods=['POST'])
def push_message():

    data = request.json
    messages = []
    if isinstance(data['messages'],list):
        # if messages is array
        for message in data['messages']:
            create_message(message)
    else:
        create_message(data['messages'])

    line_bot_api.push_message(data['user_id'],messages)

    return 'OK'

def create_message(data):
    if 'type' in data and data.type == 'image':
        message = ImageSendMessage(data['original_content_url'], data['preview_image_url'])
    else:
        message = TextSendMessage(data['message'])
    return message

def get_user_profile(user_id):
    # {
    #     "displayName": "LINE taro",
    #     "userId": "Uxxxxxxxxxxxxxx...",
    #     "pictureUrl": "http://obs.line-apps.com/...",
    #     "statusMessage": "Hello, LINE!"
    # }
    return line_bot_api.get_profile(user_id)

if __name__ == "__main__":
    app.run()