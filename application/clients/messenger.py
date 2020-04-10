import requests
from typing import List, Dict
from tornado.web import access_log as logger

#TODO: Move these out
FB_API_URL = 'https://graph.facebook.com/v3.3/me/messages'
PAGE_ACCESS_TOKEN = 'EAAd8Oi7Wz3ABAJifYCQaNJCM1OCvlWsqaDVUQjFA87h4vq7D3yGxw5rZBWlZBtxYyCUfbx7bgtA5WDOfMCmjYTeAPjVnlBRVCQioJ5jjlrEBRuADl5gF2OlsF1T5vwx2faZBtzFtraXllAX1Rc3tzHxh11snOJ9FZCRn1Kk1bQZDZD'
VERIFY_TOKEN = 'secret'


#TODO: Better error handling
class Messenger:
    """
    Client library for communicating with Graph API (Facebook).
    """
    def __init__(self, session):
        self.session = session
    
    async def send_message(self, recipient_id, message):
        """Send a response to Facebook"""
        payload = {
            'message': message,
            'recipient': {
                'id': recipient_id
            },
            'notification_type': 'regular'
        }
        auth = {
            'access_token': PAGE_ACCESS_TOKEN
        }
        async with self.session.post(
            FB_API_URL,
            params=auth,
            json=payload
        ) as r:
            status = r.status
        return status


class MessengerHelper:
    """
    Helper methods for processing data to and from facebook messenger.
    """
    @staticmethod
    def is_user_message(message) -> bool:
        condition = (
            message.get('message') and 
            message['message'].get('text') and
            not message['message'].get('is_echo')
        )
        return condition

    @staticmethod
    def verify_webhook(request_arguments: Dict) -> str:
        """
        Add message format from facebook here...
        """
        verify_token = request_arguments.get('hub.verify_token')[0]
        challenge = request_arguments.get('hub.challenge')[0]
        if verify_token.decode('utf-8') == VERIFY_TOKEN:
            logger.info('Messenger webhook validated.')
            return challenge.decode('utf-8')
        else:
            logger.info('Messenger webhook validation failed.')
            return None
    
    @staticmethod
    def format_attachment_payload(list_of_data: List[Dict]) -> Dict:
        elements = []
        for data in list_of_data:
            element = {
                'title': f"{data.get('name')} - {data.get('set_name')}",
                'image_url': data.get('image_url'),
                'subtitle': f"""Normal: {data.get('normal_price')} \n
                                Foil: {data.get('foil_price')} 
                             """,
                'default_action': {
                    'type': 'web_url',
                    'url': data.get('image_url'),
                    'webview_height_ratio': 'full',
                },
                'buttons': [
                    {
                        'type': 'web_url',
                        'url': data.get('url'),
                        'title': 'Get it @TCGPlayer',
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

    @staticmethod
    def format_text_payload(data):
        return {'text': data}