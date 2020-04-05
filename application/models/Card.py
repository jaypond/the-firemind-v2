from orator import Model
from orator.orm import accessor, has_one

class Card(Model):
    __fillable__ = [
        'card_id', 'set_id', 'name', 'clean_name', 'image_url', 'url'
    ]
    __primary_key__ = 'card_id'
    __timestamps__ = False

    @has_one
    def card_set(self):
        return CardSet
    
    @has_one
    def price(self):
        return Price
    
    @accessor
    def card_data(self):
        data = {
            'name': self.get_raw_attribute('name'),
            'image_url': self.get_raw_attribute('image_url'),
            'url': self.get_raw_attribute('url'),
            'set_name': self.card_set.name,
            'normal_price': self.price.normal_price,
            'foil_price': self.price.foil_price
        }

    @scope
    def card_name(self, query, name):
        return query.where_raw(
            f"name = '{name}' or clean_name = '{name}'"
        )
