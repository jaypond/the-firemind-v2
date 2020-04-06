from orator import Model


class CardSet(Model):
    __fillable__ = ['set_id', 'name', 'is_supplemental', 'published_on']
    __primary_key__ = 'set_id'
    __timestamps__ = False
