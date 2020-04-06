import json
from typing import List, Dict
from tornado.web import access_log as logger

from application.handler import BaseHandler
from application.models.card import Card
from application.clients.messenger import Messenger


def messenger_template_helper(list_of_data: List[Dict]) -> Dict:
    elements = []
    for data in list_of_data:
        element = {
            "title": "{} - {}".format(data.get('name'), data.get('set_name')),
            "image_url": data.get('image_url'),
            "subtitle": "Normal: ${}\nFoil: ${}".format(data.get('normal_price'), data.get('foil_price')),
            "default_action": {
                "type": "web_url",
                "url": data.get('image_url'),
                "webview_height_ratio": "full",
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": data.get('url'),
                    "title": "Get it @TCGPlayer",
                }
            ]
        }
        elements.append(element)
    messenger_payload = {
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'generic',
                'elements': elements
            }
        }
    }
    return messenger_payload


class MessengerHandler(BaseHandler):

    async def get(self):
        challenge = Messenger.verify_webhook(self.request.arguments)
        return self.write(challenge, 200)
    
    async def post(self):
        payload = json.loads(self.request.body)
        event = payload['entry'][0]['messaging']
        for x in event:
            if Messenger.is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                cards = Card.card_name(text).get()
                response = messenger_template_helper(
                    [card.card_data for card in cards]
                )
                Messenger.send_message(sender_id, response)
        return self.write("ok", 200)