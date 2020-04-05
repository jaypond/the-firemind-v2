import asyncio
import tornado.web

from tornado.options import define, options, parse_command_line
from tornado.log import enable_pretty_logging, access_log as logger

from .routes.cards import CardHandler
from .clients.redis import Redis
from .clients.tcgplayer import TCGPlayer

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

#TODO: import config cleaner; make it async
class Application:
    def __init__(self):
        pass

    def make_app(self) -> tornado.web.Application:
        config = {
            'session': Redis('127.0.0.1'),
            'resource': TCGPlayer(),
            'debug': True
        }
        routes = [
            (r"/cards", CardHandler)
        ]
        return tornado.web.Application(routes, **config)

    def start(self):
        app = self.make_app()
        enable_pretty_logging()
        app.listen(options.port)
        logger.info('Server is now listening for requests...')
        tornado.ioloop.IOLoop.current().start()
