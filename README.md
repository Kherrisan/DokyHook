# DokyHook
A tornado-based api invoked by github webhook.

Usage step:
1. Import the AbstractWebHook and WebHookInjector.
2. Define a new class that extends the AbstractWebHook and overwrite the functions you need.
3. In main function,inject the customed hook class to the tornado application object.

If you need to specified secret to check the integity with digest sent by github,just pass the secret as the paramater.

Usage example:

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
        
This example shows how to pull the respository automatically when a commit take place.