from application.app import Application
import tornado.options
#TODO: rename application object

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    app.start()