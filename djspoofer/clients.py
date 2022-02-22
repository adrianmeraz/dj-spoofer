import logging

from djstarter.clients import Http2Client

logger = logging.getLogger(__name__)


class SpoofedDesktopClient(Http2Client):
    def __init__(self, fingerprint, *args, **kwargs):
        self.fingerprint = fingerprint
        self.proxies = self.init_proxies()
        super().__init__(proxies=self.proxies, *args, **kwargs)

    def init_headers(self):
        return {
            # 'authority': '',
            # 'sec_ch_ua': self.sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': self.sec_ch_ua_platform,
            'upgrade-insecure-requests': '1',
            'user-agent': self.fingerprint.user_agent,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
        }

    def init_proxies(self):
        if proxy := self.fingerprint.proxy:
            return {
                'http://': proxy.http_url,
                'https://': proxy.https_url
            }
        return dict()

    def send(self, *args, **kwargs):
        self.headers.pop('Accept-Encoding', None)
        self.headers.pop('Connection', None)
        return super().send(*args, **kwargs)

    @staticmethod
    def url_authority(url):
        #   TODO parse hostname and use it
        return

    @property
    def sec_ch_ua(self):
        return

    @property
    def sec_ch_ua_platform(self):
        return
