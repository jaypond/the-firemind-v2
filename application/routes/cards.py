import json

from application.handler import BaseHandler


class CardHandler(BaseHandler):

    async def get(self):
        self.write("HELLO WORLD")