import json
import requests
import aiohttp

from tornado.web import access_log as logger
from typing import List, Dict, Tuple
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
def reauthenticate(f):
    @wraps(f)
    async def wrapper(self, *args, **kwargs):
        if (
            not hasattr(self, 'token_expiry') or 
            datetime.now() > self.token_expiry
        ):
            await self.authenticate()
        return await f(self, *args, **kwargs)
    return wrapper


#TODO: raise error in case of authentication problems
class TCGPlayer:
    """
    Client library for communicating with TCGPlayer's API.
    :param session: Async http session
    """
    def __init__(self, session):
        self.session = session
        self.access_token = None

    @property
    def headers(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        return headers

    async def authenticate(self):
        """
        Authenticate
        """
        logger.info(' AIO - Authenticating - TCGPlayer API...')
        data = {
            'grant_type': 'client_credentials',
            'client_id': PUBLIC_KEY,
            'client_secret': PRIVATE_KEY
        }
        async with self.session.post(
            f'{TCGPLAYER_API_URL}/token', data=data
        ) as r:
            status = r.status
            content = await r.json()
        if status == 200:
            self.access_token = content.get('access_token')
            self.token_expiry = datetime.strptime(
                content.get('.expires'), DATETIME_FORMAT
            )
            logger.info('AIO - Authenticated! - TCGPlayer API')

    #TODO: Add handling if status is not 200
    @reauthenticate
    async def cards(self, offset=0, limit=100) -> List[Dict]:
        """
        Retrieves a list of cards from TCGPlayer
        """
        params = {
            'offset': offset,
            'limit': limit,
            'categoryId': MTG_CATEGORY_ID,
            'productTypes': 'Cards'
        }
        async with self.session.get(
            f'{TCGPLAYER_API_URL}/catalog/products', 
            headers=self.headers,
            params=params
        ) as r:
            status = r.status
            content = await r.json()
        if status == 200:
            cards = content.get('results')
            return cards
        else:
            raise NotImplementedError
    
    @reauthenticate
    async def card_sets(self, offset=0, limit=100) -> List[Dict]:
        """
        Retrieves a list of cards from TCGPlayer
        """
        params = {
            'offset': offset,
            'limit': limit,
        }
        async with self.session.get(
            f'{TCGPLAYER_API_URL}/catalog/categories/{MTG_CATEGORY_ID}/groups', 
            headers=self.headers,
            params=params
        ) as r:
            status = r.status
            content = await r.json()
        if status == 200:
            card_sets = content.get('results')
            return card_sets
        else:
            raise NotImplementedError
    
    @reauthenticate
    async def prices(self, card_ids: List[int]) -> List[Dict]:
        """
        Retrieves a list of prices from TCGPlayer
        """
        card_ids = ','.join(map(str, card_ids))
        async with self.session.get(
            f'{TCGPLAYER_API_URL}/pricing/product/{card_ids}',
            headers=self.headers
        ) as r:
            status = r.status
            content = await r.json()
        if status == 200:
            prices = content.get('results')
            return prices
        else:
            return NotImplementedError
