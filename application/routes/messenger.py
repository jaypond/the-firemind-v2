from tornado.web import access_log as logger
from application.handler import BaseHandler
from application.models.cards import Card


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
    return elements


class MessengerHandler(BaseHandler):

    async def get(self):
        pass
    
    async def post(self):
        pass
    