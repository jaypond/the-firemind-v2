import aiohttp
import tornado.web
import tornado.ioloop
from random import randint

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        """
        Initialize needed services
        :resource: resource to retrieve cards from (tcgplayer).
        :cache: Redis instance for caching.
        """
        self.resource = self.settings.get('resource')
        self.messenger = self.settings.get('messenger')
        self.cache = self.settings.get('cache')

    def write(self, data, status_code=None):
        """
        Overriding default write function of tornado.
        If data is a list, wrap it around a dictionary since tornado
        does not allow lists due to security reasons.
        Also sets the status code if given ex. write(data, 202)

        :param data: data to be written/returned to requester.
        :param status_code: status code to return to the requester.
        """
        if isinstance(data, list):
            data = {'data': data}
        if status_code:
            self.set_status(status_code)
        super(BaseHandler, self).write(data)
