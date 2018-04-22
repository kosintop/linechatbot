import io
from flask import Flask, request, abort
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

    print(request.headers)
    print(request.get_data(as_text=True))

    return request.get_data(as_text=True)

    #return send_file(io.BytesIO(request.data),mimetype='image/jpeg', attachment_filename='myfile.jpg')


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
def imagemap_4600():
    return send_file('460.jpg', mimetype='image/jpg')


@app.route("/imagemap/700", methods=['GET'])
def imagemap_7000():
    return send_file('700.jpg', mimetype='image/jpg')


@app.route("/imagemap/1040", methods=['GET'])
def imagemap_10400():
    return send_file('1040.jpg', mimetype='image/jpg')


if __name__ == "__main__":
    app.run()
