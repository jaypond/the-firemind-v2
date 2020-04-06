import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = self.settings.get('session')
        self.resource = self.settings.get('resource')
    
    #TODO: add status code handling inside
    def write(self, data, status_code=None):
        if isinstance(data, list):
            data = {'data': data}
        if status_code:
            self.set_status(status_code)
        super(BaseHandler, self).write(data)