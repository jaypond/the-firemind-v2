import json
from typing import List, Dict
from tornado.web import access_log as logger

from application.handler import BaseHandler
from application.models.card import Card
from application.clients.messenger import Messenger, MessengerHelper

#TODO: cleanup; jsondumps output?

class MessengerHandler(BaseHandler):
    async def get(self):
        challenge = MessengerHelper.verify_webhook(self.request.arguments)
        return self.write(challenge, 200)
    
    async def post(self):
        """
        Messenger snippet to receive user messages
        """
        payload = json.loads(self.request.body)
        event = payload['entry'][0]['messaging']
        for x in event:
            if MessengerHelper.is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                cards = Card.has('card_set').card_name(text).get()
                if cards:
                    response = MessengerHelper.format_attachment_payload(
                        [card.card_data for card in cards]
                    )
                else:
                    #TODO: extract functionality.
                    response = MessengerHelper.format_text_payload(
                        f'{text} not found. Please try again.'
                    )
                await self.messenger.send_message(sender_id, response)
        return self.write('ok', 200)
