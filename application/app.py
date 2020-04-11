import aiohttp
import tornado.web
import tornado.ioloop

from tornado.options import define, options, parse_command_line
from tornado.log import enable_pretty_logging, access_log as logger

from .routes.cards import CardHandler, CardSetHandler, PriceHandler, TestHandler
from .routes.messenger import MessengerHandler
from .clients.redis import Redis
from .clients.tcgplayer import TCGPlayer
from .clients.messenger import Messenger

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

#TODO: import config cleaner
class Application:
    def __init__(self):
        pass

    def make_app(self) -> tornado.web.Application:
        session = aiohttp.ClientSession()
        config = {
            'cache': Redis('cache'),
            'resource': TCGPlayer(session),
            'messenger': Messenger(session),
            'debug': True
        }
        routes = [
            (r"/test", TestHandler),
            (r"/cards", CardHandler),
            (r"/card_sets", CardSetHandler),
            (r"/prices", PriceHandler),
            (r"/webhook", MessengerHandler)
        ]
        return tornado.web.Application(routes, **config)

    def start(self):
        app = self.make_app()
        enable_pretty_logging()
        app.listen(options.port)
        logger.info(f'Server is now listening for requests...')
        tornado.ioloop.IOLoop.current().start()
