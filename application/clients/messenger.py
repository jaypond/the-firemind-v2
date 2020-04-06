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

    @staticmethod
    def is_user_message(message):
        condition = (
            message.get('message') and 
            message['message'].get('text') and
            not message['message'].get('is_echo')
        )
        return condition

    @staticmethod
    def verify_webhook(request_arguments: Dict):
        verify_token = request_arguments.get('hub.verify_token')[0]
        challenge = request_arguments.get('hub.challenge')[0]
        if verify_token.decode('utf-8') == VERIFY_TOKEN:
            logger.info('Messenger webhook validated.')
            return challenge.decode('utf-8')
        else:
            return logger.info('Messenger webhook validation failed.')
    
    @staticmethod
    def send_message(recipient_id, message):
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
        response = requests.post(
            FB_API_URL,
            params=auth,
            json=payload
        )
        print(response.status_code)
        return "Success"
