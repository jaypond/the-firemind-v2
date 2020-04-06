from orator import Model
from orator.orm import accessor, has_one, has_many, scope
from .card_set import CardSet
from .price import Price

class Card(Model):
    __fillable__ = [
        'card_id', 'set_id', 'name', 'clean_name', 'image_url', 'url'
    ]
    __primary_key__ = 'card_id'
    __timestamps__ = False

    @has_one('set_id', 'set_id')
    def card_set(self):
        return CardSet
    
    @has_many
    def prices(self):
        return Price
    
    @accessor
    def foil_price(self):
        price_object = next(
            filter(lambda x: x.card_type == 'Foil', self.prices), None
        )
        return price_object.price
    
    @accessor
    def normal_price(self):
        price_object = next(
            filter(lambda x: x.card_type == 'Normal', self.prices), None
        )
        return price_object.price
    
    @accessor
    def card_data(self):
        data = {
            'name': self.get_raw_attribute('name'),
            'image_url': self.get_raw_attribute('image_url'),
            'url': self.get_raw_attribute('url'),
            'set_name': self.card_set.name,
            'normal_price': self.normal_price,
            'foil_price': self.foil_price
        }
        return data

    @scope
    def card_name(self, query, name):
        return query.where_raw(
            f"name = '{name}' or clean_name = '{name}'"
        )
