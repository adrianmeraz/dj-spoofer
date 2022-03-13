import logging
import random
from abc import ABC

import httpx
from djstarter.clients import Http2Client
from ua_parser import user_agent_parser
from ssl import TLSVersion

logger = logging.getLogger(__name__)


class DesktopClient(ABC, Http2Client):
    CIPHERS = ':'.join([
        "ECDHE+AESGCM",
        "ECDHE+CHACHA20",
        "DHE+AESGCM",
        "DHE+CHACHA20",
        "ECDH+AESGCM",
        "DH+AESGCM",
        "ECDH+AES",
        "DH+AES",
        "RSA+AESGCM",
        "RSA+AES",
    ])

    def __init__(self, fingerprint, *args, **kwargs):
        self.fingerprint = fingerprint
        self.user_agent = fingerprint.user_agent
        self.proxies = self.init_proxies()
        super().__init__(proxies=self.proxies, verify=self.ssl_context(), *args, **kwargs)

    def send(self, *args, **kwargs):
        self.headers.pop('Accept-Encoding', None)
        self.headers.pop('Connection', None)
        return super().send(*args, **kwargs)

    def ssl_context(self):
        context = httpx.create_ssl_context(http2=True)
        context.set_alpn_protocols(['h2'])
        context.minimum_version = TLSVersion.TLSv1_2
        context.set_ciphers(self.CIPHERS)
        return context

    def init_proxies(self):
        if proxy := self.fingerprint.proxy:
            return {
                'http://': proxy.http_url,
                'https://': proxy.https_url
            }
        return dict()


def grease_cipher():
    val = random.randint(1, 8)
    return f'TLS_GREASE_IS_THE_WORD_{val}A'


class DesktopChromeClient(DesktopClient):
    CIPHERS = ':'.join([
        grease_cipher(),
        'AES128-GCM-SHA256',
        'AES256-GCM-SHA384',
        'CHACHA20-POLY1305-SHA256',     # TODO Not implemented in ssl module
        'ECDHE-ECDSA-AES128-GCM-SHA256',
        'ECDHE-RSA-AES128-GCM-SHA256',
        'ECDHE-ECDSA-AES256-GCM-SHA384',
        'ECDHE-RSA-AES256-GCM-SHA384',
        'ECDHE-ECDSA-CHACHA20-POLY1305',
        'ECDHE-RSA-CHACHA20-POLY1305',
        'ECDHE-RSA-AES128-SHA',
        'ECDHE-RSA-AES256-SHA',
        'AES128-GCM-SHA256',
        'AES256-GCM-SHA384',
        'AES128-SHA',
        'AES256-SHA',
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    @property
    def sec_ch_ua(self):
        version = UserAgentParser(self.user_agent).browser_major_version
        return f'" Not;A Brand";v="99", "Google Chrome";v="{version}", "Chromium";v="{version}"'

    @property
    def sec_ch_ua_platform(self):
        platform = UserAgentParser(self.user_agent).platform
        return f'"{platform}"'


class DesktopFirefoxClient(DesktopClient):
    CIPHERS = ':'.join([
        'AES128-GCM-SHA256',
        'CHACHA20-POLY1305-SHA256',     # TODO Not implemented in ssl module
        'AES256-GCM-SHA384',
        'ECDHE-ECDSA-AES128-GCM-SHA256',
        'ECDHE-RSA-AES128-GCM-SHA256',
        'ECDHE-ECDSA-CHACHA20-POLY1305',
        'ECDHE-RSA-CHACHA20-POLY1305',
        'ECDHE-ECDSA-AES256-GCM-SHA384',
        'ECDHE-RSA-AES256-GCM-SHA384',
        'ECDHE-ECDSA-AES256-SHA',
        'ECDHE-ECDSA-AES128-SHA',
        'ECDHE-RSA-AES128-SHA',
        'ECDHE-RSA-AES256-SHA',
        'AES128-GCM-SHA256',
        'AES256-GCM-SHA384',
        'AES128-SHA',
        'AES256-SHA',
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_headers(self):
        return {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
        }


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