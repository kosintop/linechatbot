import io
import json
import requests
from flask import Flask, request, abort
from flask import send_file

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import ImageMessage
from linebot.models import LocationSendMessage
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage

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

@app.route("/test", methods=['POST'])
def test_endpoint():
    print("testing")
    return send_file(io.BytesIO(request.data))

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_profile = get_user_profile(event.source.user_id)
    reply_token = event.reply_token
    #reply = "Hello " + user_profile.display_name + ", your message was " + event.message.text + ", your user_id is " + user_profile.user_id

    data = {
        "USERID": event.source.user_id,
        "MESSAGE": event.message.text,
        "TOKENID": event.reply_token
    }

    response = requests.post("http://inventech.co.th/dbo_stonline/B2BSERVICES.svc/ASKBOBV2",json=data)

    response_data = response.json()
    print(response_data)
    message = create_message(json.loads(response_data))
    line_bot_api.reply_message(reply_token,message)


@handler.add(MessageEvent,message=ImageMessage)
def handle_image_message(event):
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    content_type = message_content.content_type
    content = message_content.content
    r = requests.post('https://line-chatbot-kos.herokuapp.com/test', files={'image': content})
    return 'OK'

@app.route("/push_message", methods=['POST'])
def push_message():
    data = request.json
    messages = []

    if isinstance(data['messages'],list):
        # if messages is array
        for message in data['messages']:
            messages.append(create_message(message))
    else:
        messages.append(create_message(data['messages']))

    line_bot_api.push_message(data['to'],messages)
    return 'OK'


def create_message(data):

    if data['type'] == 'text':
        message = TextSendMessage(text=data['text'])
    elif data['type'] == 'image':
        message = ImageSendMessage(original_content_url=data['originalContentUrl'],preview_image_url=data['previewImageUrl'])
    elif data['type'] == 'location':
        message = LocationSendMessage(title=data['title'],address=data['address'],latitude=data['latitude'],longitude=data['longitude'])
    elif data['type'] == 'video':
        pass
    elif data['type'] == 'audio':
        pass
    elif data['type'] == 'sticker':
        pass
    elif data['type'] == 'imagemap':
        pass
    elif data['type'] == 'tempalte':
        pass
    else:
        raise TypeError

    return message


def get_user_profile(user_id):
    """
    Example of user_profile object
    {
        "display_name": "LINE taro",
        "user_id": "Uxxxxxxxxxxxxxx...",
        "picture_url": "http://obs.line-apps.com/...",
        "status_message": "Hello, LINE!"
    }
    """
    return line_bot_api.get_profile(user_id)

if __name__ == "__main__":
    app.run()
