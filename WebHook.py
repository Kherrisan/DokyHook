import tornado.ioloop
import tornado.web
import hmac


class WebHookInjector(object):

    @staticmethod
    def inject(url, app, webhook, secret=None):
        if secret:
            webhook.hmac_o = hmac.new(bytes(secret))
        if isinstance(webhook, type):
            webhook = webhook.__call__()

        class WebHookHandler(tornado.web.RequestHandler):
            def post(self, *args, **kwargs):
                webhook.handle_post(self.request)

        app.add_handlers(".*$", [(url, WebHookHandler)])
        return webhook


class AbstractWebHook(object):
    def __init__(self):
        self.hmac_o = None

    def handle_post(self, request):
        if not request.headers:
            return
        headers = request.headers
        if "X-GitHub-Event" not in headers:
            return
        event_type = headers["X-GitHub-Event"]
        if (self.hmac_o and "X-Hub-Signature" in headers.keys()) or (
                not self.hmac_o and "X-Hub-Signature" not in headers.keys()):
            digit = headers["X-Hub-Signature"].split("=")[1]
            self.hmac_o.update(bytes(request.body))
            if self.hmac_o.hexdigest() != digit:
                print("Signature error.")
                return
        else:
            print("Signature configuartion error.")
            return
        payload = request.body
        callback = self.__dispatch(event_type)
        if not callback:
            callback(self, payload)
        return

    def __dispatch(self, event_type):
        if event_type == "commit_comment":
            return self.on_commit_comment
        elif event_type == "create":
            return self.on_create
        elif event_type == "delete":
            return self.on_delete
        elif event_type == "push":
            return self.on_push
        else:
            return None

    def on_commit_comment(self, payload):
        pass

    def on_create(self, payload):
        pass

    def on_delete(self, payload):
        pass

    def on_fork(self, payload):
        pass

    def on_issue_comment(self, payload):
        pass

    def on_issue(self, payload):
        pass

    def on_labele(self, payload):
        pass

    def on_milestone(self, payload):
        pass

    def on_pull_request(self, payload):
        pass

    def on_push(self, payload):
        pass

    def on_release(self, payload):
        pass

    def on_watch(self, payload):
        pass
