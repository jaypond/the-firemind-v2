import json
import requests

from typing import List, Dict
from datetime import datetime
from functools import wraps, cached_property

#TODO: move these to docker-compose
TCGPLAYER_API_VERSION = 'v1.37.0'
TCGPLAYER_API_URL = f'http://api.tcgplayer.com/{TCGPLAYER_API_VERSION}'
MTG_CATEGORY_ID = 1
PUBLIC_KEY = 'F7345302-4B66-4A3F-BE49-333C4CB7057C'
PRIVATE_KEY = '3525C23D-9C8D-4919-AD79-67A0F07F92EA'
DATETIME_FORMAT = r'%a, %d %b %Y %H:%M:%S %Z'

#TODO: better name for this decorator which reauthenticates when needed
def request_access(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if (
            not hasattr(self, 'token_expiry') or 
            datetime.now() > self.token_expiry
        ):
            self.authenticate()
        return f(self, *args, **kwargs)
    return wrapper


class TCGPlayer:
    """
    Client library for communicating with TCGPlayer's API.
    """
    @cached_property
    def session(self):
        return requests.Session()

    def authenticate(self):
        """
        Authenticate
        """
        data = {
            'grant_type': 'client_credentials',
            'client_id': PUBLIC_KEY,
            'client_secret': PRIVATE_KEY
        }
        r = self.session.post(
            f'{TCGPLAYER_API_URL}/token', data=data
        )
        if r.status_code == 200:
            content = r.json()
            self.access_token = content.get('access_token')
            self.session.headers.update(
                {'Authorization': f'Bearer {self.access_token}'}
            )
            self.token_expiry = datetime.strptime(
                content.get('.expires'), DATETIME_FORMAT
            )
        else:
            raise NotImplementedError

    @request_access
    def cards(self, offset=0, limit=100) -> List[Dict]:
        """
        Retrieves a list of cards from TCGPlayer
        """
        params = {
            'offset': offset,
            'limit': limit,
            'category': MTG_CATEGORY_ID,
            'productTypes': 'Cards'
        }
        print(self.session.headers)
        r = self.session.get(
            f'{TCGPLAYER_API_URL}/catalog/products',
            params=params
        )
        if r.status_code == 200:
            content = r.json()
            cards = content.get('results')
            return cards
        else:
            raise NotImplementedError
    
    @request_access
    def card_sets(self, offset=0, limit=100) -> List[Dict]:
        """
        Retrieves a list of card_sets from TCGPlayer
        """
        params = {
            'offset': offset,
            'limit': limit,
        }
        r = self.session.get(
            f'{TCGPLAYER_API_URL}/catalog/categories/{MTG_CATEGORY_ID}/groups',
            params=params
        )
        if r.status_code == 200:
            content = r.json()
            card_sets = content.get('results')
            return card_sets
        else:
            raise NotImplementedError
    
    @request_access
    def prices(self, card_ids: List[int]) -> List[Dict]:
        """
        Retrieves a list of prices from TCGPlayer
        """
        card_ids = ','.join(map(str, card_ids))
        r = self.session.get(
            f'{TCGPLAYER_API_URL}/pricing/product/{card_ids}'
        )
        if r.status_code == 200:
            content = r.json()
            card_sets = content.get('results')
            return card_sets
        else:
            raise NotImplementedError
