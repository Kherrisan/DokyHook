import tornado.ioloop
import subprocess
import os

from WebHook import AbstractWebHook, WebHookInjector


class WebHook(AbstractWebHook):

    def on_push(self, payload):
        print("on_push")


class AutoPullHook(AbstractWebHook):
    REPO_PATH = "/var/www/test/webhook"

    def __init__(self):
        super().__init__()

    def on_push(self, payload):
        print("Repo push hook.")
        subprocess.call(["git", "pull"], cwd=AutoPullHook.REPO_PATH)


if __name__ == '__main__':
    app = tornado.web.Application()
    WebHookInjector.inject("/test/webhook", app, AutoPullHook, "the secret")
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
