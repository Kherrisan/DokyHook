import tornado.ioloop

from WebHook import AbstractWebHook, WebHookInjector


class WebHook(AbstractWebHook):

    def on_push(self, payload):
        print("on_push")


if __name__ == '__main__':
    app = tornado.web.Application()
    WebHookInjector.inject("/test/webhook", app, WebHook, "zou970514")
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
