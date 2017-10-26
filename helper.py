from linebot.models import ImageSendMessage
from linebot.models import LocationSendMessage
from linebot.models import TextSendMessage


def create_messages(data_list):
    message_list = []
    for data in data_list:
        message_list.append(create_message(data))
    return message_list

def create_message(data):
    if data['type'] == 'text':
        message = TextSendMessage(text=data['text'])
    elif data['type'] == 'image':
        message = ImageSendMessage(original_content_url=data['originalContentUrl'], preview_image_url=data['previewImageUrl'])
    elif data['type'] == 'location':
        message = LocationSendMessage(title=data['title'], address=data['address'], latitude=data['latitude'], longitude=data['longitude'])
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
        raise TypeError('invalid message type, found ' + data['type'])

    return message