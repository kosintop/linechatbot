from linebot.models import ImageSendMessage
from linebot.models import LocationSendMessage
from linebot.models import TextSendMessage
from linebot.models import ImagemapSendMessage
from linebot.models.imagemap import ImagemapAction, BaseSize, URIImagemapAction, MessageImagemapAction,ImagemapArea

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
    elif data['type'] == 'template':
        pass
    else:
        raise TypeError('invalid message type, found ' + data['type'])

    return message


def create_imagemap():
    message = ImagemapSendMessage(
        base_url='https://pbs.twimg.com/profile_images/846801302378078208/Xihz3l5J_400x400.jpg',
        base_size=BaseSize(height=400,width=400),
        actions=[
                URIImagemapAction(
                    link_uri='https://www.google.com/',
                    area=ImagemapArea(
                        x=0, y=0, width=200, height=200
                    )
                ),
                MessageImagemapAction(
                    text='blue',
                    area=ImagemapArea(
                        x=200, y=0, width=200, height=200
                    )
                ),
                MessageImagemapAction(
                    text='yellow',
                    area=ImagemapArea(
                        x=0, y=200, width=200, height=200
                    )
                ),
                URIImagemapAction(
                    link_uri='https://www.stackoverflow.com/',
                    area=ImagemapArea(
                        x=200, y=200, width=200, height=200
                    )
                ),
            ])
    return message