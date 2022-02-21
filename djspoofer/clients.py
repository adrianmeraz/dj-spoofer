import logging

from djstarter.clients import Http2Client

logger = logging.getLogger(__name__)


class SpoofedDesktopClient(Http2Client):
    def __init__(self, fingerprint, *args, **kwargs):
        self.fingerprint = fingerprint
        self.proxies = {
            'http://': fingerprint.proxy.http_url,
            'https://': fingerprint.proxy.https_url
        }
        super().__init__(proxies=self.proxies, *args, **kwargs)

    def init_headers(self):
        return {
            'accept': 'application/json',
            'user-agent': self.fingerprint.user_agent
        }
