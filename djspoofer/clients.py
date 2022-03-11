import logging

from djstarter.clients import Http2Client
from ua_parser import user_agent_parser

logger = logging.getLogger(__name__)


class SpoofedChromeClient(Http2Client):
    def __init__(self, fingerprint, *args, **kwargs):
        self.fingerprint = fingerprint
        self.user_agent = fingerprint.user_agent
        self.proxies = self.init_proxies()
        super().__init__(proxies=self.proxies, *args, **kwargs)

    def init_headers(self):
        return {
            'sec_ch_ua': self.sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': self.sec_ch_ua_platform,
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent,
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

    @property
    def sec_ch_ua(self):
        version = UserAgentParser(self.user_agent).browser_major_version
        return f'" Not;A Brand";v="99", "Google Chrome";v="{version}", "Chromium";v="{version}"'

    @property
    def sec_ch_ua_platform(self):
        platform = UserAgentParser(self.user_agent).platform
        return f'"{platform}"'


class SpoofedFirefoxClient(Http2Client):
    def __init__(self, fingerprint, *args, **kwargs):
        self.fingerprint = fingerprint
        self.user_agent = fingerprint.user_agent
        self.proxies = self.init_proxies()
        super().__init__(proxies=self.proxies, *args, **kwargs)

    def init_headers(self):
        return {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
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


class UserAgentParser:
    def __init__(self, user_agent):
        self.ua_parser = user_agent_parser.Parse(user_agent)

    @property
    def browser(self):
        return self.ua_parser['user_agent']['family']

    @property
    def browser_major_version(self):
        return self.ua_parser['user_agent']['major']

    @property
    def platform(self):
        return self.ua_parser['os']['family']