import io

import requests
from flask import Flask, request, abort, redirect
from flask import send_file
from handler import event_handler, line_bot_api
from linebot.exceptions import InvalidSignatureError

from helper import create_message

app = Flask(__name__)


@app.route("/callback", methods=['POST'])
def callback():
    """
    Main callback.
    Receive event from Line platform and delegate event to respective handler
    :return Http response status:
    """
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        event_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@app.route("/test", methods=['GET'])
def test_endpoint():
    print('header')
    print(request.get_data(as_text=True))
    code = request.args.get('code')
    response = requests.post('https://api.line.me/oauth2/v2.1/token',data={
        'grant_type':'authorization_code',
        'code':code,
        'redirect_uri':'https://salestools-chatbot.herokuapp.com/test2',
        'client_id':'1581119181',
        'client_secret':'a3dc6d57957ac8c0c8ebe88fc7687d99',
    })
    print(response.json())
    token = response.json()['access_token']
    response2 = requests.get('https://api.line.me/v2/profile',headers={'Authorization': 'Bearer %s' % token})

    return response2.json()
    #return send_file(io.BytesIO(request.data),mimetype='image/jpeg', attachment_filename='myfile.jpg')


@app.route("/test2", methods=['GET'])
def test_endpoint2():
    return 'test2'


@app.route("/push_message", methods=['POST'])
def push_message():
    """
    API for pushing message to client, incoming request should contain json.

    json = {
        'to': string of user_id to push message to
        'messages': array of message to push - 5 maximum
    }

    :return Http response status:
    """
    data = request.json
    messages = []

    if isinstance(data['messages'],list):
        for message in data['messages']:
            messages.append(create_message(message))
    else:
        messages.append(create_message(data['messages']))

    line_bot_api.push_message(data['to'],messages)
    return 'OK'


@app.route("/imagemap/240", methods=['GET'])
def imagemap_240():
    return send_file('240.jpg', mimetype='image/jpg')


@app.route("/imagemap/300", methods=['GET'])
def imagemap_300():
    return send_file('300.jpg', mimetype='image/jpg')


@app.route("/imagemap/460", methods=['GET'])
def imagemap_460():
    return send_file('460.jpg', mimetype='image/jpg')


@app.route("/imagemap/700", methods=['GET'])
def imagemap_700():
    return send_file('700.jpg', mimetype='image/jpg')


@app.route("/imagemap/1040", methods=['GET'])
def imagemap_1040():
    return send_file('1040.jpg', mimetype='image/jpg')


if __name__ == "__main__":
    app.run()
