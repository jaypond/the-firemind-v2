from orator import Model


class Price(Model):
    __fillable__ = ['card_id', 'normal_price', 'foil_price']
    __timestamps__ = False
