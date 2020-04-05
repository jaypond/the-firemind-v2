import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def __initialize__(self, session, resource):
        self.resource = resource
        self.session = session
    
    def write(self, data):
        if isinstance(data, list):
            data = {'data': data}

        super(BaseHandler, self).write(data)