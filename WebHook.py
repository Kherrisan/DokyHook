import tornado.ioloop
import tornado.web
import hmac
import hashlib
import logging


class WebHookInjector(object):
    """

    """

    @staticmethod
    def inject(url, app, webhook, secret=None):
        """
        Inject the new webhook handle into tornado app.
        :param url:The url which maps to the request handle.
        :param app:Tornado app object,which could already hold several request handles.
        :param webhook:The hook class which extends the AbstractWebHook and overrides specific callback functions.
        :param secret:None if no secret is configured,if is not None,the webhook object would check the digest everytime receiving post request.
        :return:webhook object.
        """
        if isinstance(webhook, type):
            webhook = webhook.__call__()
        if secret:
            webhook.secret = secret

        class WebHookHandler(tornado.web.RequestHandler):
            def post(self, *args, **kwargs):
                webhook.handle_post(self.request)

        app.add_handlers(".*$", [(url, WebHookHandler)])
        return webhook


class AbstractWebHook(object):
    def __init__(self):
        """
        You can override customed constructor but remember to invoke the constructor of super class in the first line.
        """
        self.secret = None
        self.on_hook_init()

    def handle_post(self, request):
        """

        :param request:
        :return:
        """
        logging.debug("Received post request.")
        if not request.headers:
            return
        headers = request.headers
        if "X-GitHub-Event" not in headers:
            return
        event_type = headers["X-GitHub-Event"]
        if (self.secret and "X-Hub-Signature" in headers.keys()) or (
                not self.secret and "X-Hub-Signature" not in headers.keys()):
            digit = headers["X-Hub-Signature"].split("=")[1]
            hmac_o = hmac.new(bytes(self.secret, "utf-8"), digestmod=hashlib.sha1)
            hmac_o.update(bytes(request.body))
            if hmac_o.hexdigest() != digit:
                logging.error("Digest of payload is inconsistent with the signature in the request headers.")
                return
        else:
            logging.error("Github and programme secret configuration inconsistent.")
            return
        payload = request.body
        logging.info("Payload :%s" % (payload,))
        callback = self.__dispatch(event_type)
        if callback:
            callback(payload)
        return

    def __dispatch(self, event_type):
        """

        :param event_type:
        :return:
        """
        logging.info("Event type :%s" % (event_type,))
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

    def on_hook_init(self):
        """

        :return:
        """
        pass

    def on_commit_comment(self, payload):
        """
        Any time a Commit is commented on.
        :param payload:
        :return:
        """
        pass

    def on_create(self, payload):
        """
        Any time a Branch or Tag is created.
        :param payload:
        :return:
        """
        pass

    def on_delete(self, payload):
        """
        Any time a Branch or Tag is deleted.
        :param payload:
        :return:
        """
        pass

    def on_fork(self, payload):
        """
        Any time a Repository is forked.
        :param payload:
        :return:
        """
        pass

    def on_issue_comment(self, payload):
        """
        Any time a comment on an issue is created, edited, or deleted.
        :param payload:
        :return:
        """
        pass

    def on_issue(self, payload):
        """
        Any time an Issue is assigned, unassigned, labeled, unlabeled, opened, edited,
        milestoned, demilestoned, closed, or reopened.
        :param payload:
        :return:
        """
        pass

    def on_label(self, payload):
        """
        Any time a Label is created, edited, or deleted.
        :param payload:
        :return:
        """
        pass

    def on_milestone(self, payload):
        """
        Any time a Milestone is created, closed, opened, edited, or deleted.
        :param payload:
        :return:
        """
        pass

    def on_pull_request(self, payload):
        """
        Any time a pull request is assigned, unassigned, labeled, unlabeled, opened,
        edited, closed, reopened, or synchronized (updated due to a new push in the
        branch that the pull request is tracking).
        Also any time a pull request review is requested, or a review request is removed.
        :param payload:
        :return:
        """
        pass

    def on_push(self, payload):
        """
        Any Git push to a Repository, including editing tags or branches.
        Commits via API actions that update references are also counted.
        This is the default event.
        :param payload:
        :return:
        """
        pass

    def on_release(self, payload):
        """
        Any time a Release is published in a Repository.
        :param payload:
        :return:
        """
        pass

    def on_watch(self, payload):
        """
        Any time a User stars a Repository.
        :param payload:
        :return:
        """
        pass
