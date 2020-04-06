import json
from tornado.web import access_log as logger
from orator.exceptions.orm import ModelNotFound

from application.handler import BaseHandler
from application.models import db
from application.models.card import Card
from application.models.card_set import CardSet
from application.models.price import Price


#TODO: global variables for tables, error handling


class CardHandler(BaseHandler):

    async def get(self):
        try:
            card = Card.find_or_fail(193288)
            self.write(card.card_data)
        except ModelNotFound:
            self.set_status(404)
            self.write("Card not found")
    
    async def post(self):
        """
        Retrieve cards from TCGPlayer and add to database via Orator.
        """
        offset = 0
        cards = self.resource.cards(offset=offset)
        while cards:
            card_data = [
                {
                    'card_id': card.get('productId'),
                    'set_id': card.get('groupId'),
                    'name': card.get('name'),
                    'clean_name': card.get('cleanName'),
                    'image_url': card.get('imageUrl'),
                    'url': card.get('url')
                }
                for card in cards
            ]
            db.table('cards').insert(card_data)
            logger.info(f'{offset} cards updated')
            offset += 100
            cards = self.resource.cards(offset=offset)
        return self.set_status(201)


class CardSetHandler(BaseHandler):
    async def post(self):
        """
        Retrieve card sets from TCGPlayer and add to the database via
        Orator. Since there are only a few card sets, we can get away
        with using the ORM to insert these into the database.
        """
        offset = 0
        card_sets = self.resource.card_sets(offset=offset)
        while card_sets:
            for card_set in card_sets:
                CardSet.create(
                    name=card_set.get('name'),
                    set_id=card_set.get('groupId'),
                    published_on=card_set.get('publishedOn'),
                    is_supplemental=card_set.get('isSupplemental')
                )
            offset += 100
            card_sets = self.resource.card_sets(offset=offset)
        return self.set_status(201)


class PriceHandler(BaseHandler):
    async def post(self):
        """
        Retrieve prices from TCGPlayer and add to the database via
        Orator. Will use a raw statement to speed up the update.
        """
        cards_updated = 0
        with db.transaction():
            db.table('prices').delete()
            for cards in Card.chunk(100):
                card_ids = [card.card_id for card in cards]
                prices = self.resource.prices(card_ids)

                price_data = [
                    {
                        'card_id': price.get('productId'),
                        'price': price.get('midPrice'),
                        'card_type': price.get('subTypeName')
                    }
                    for price in prices
                ]
                db.table('prices').insert(price_data)
                cards_updated += len(card_ids)
                logger.info(f'{cards_updated} cards updated')
        
        return self.set_status(201)
