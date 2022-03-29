import logging
import random
from abc import ABC
from ssl import Options, TLSVersion

import httpx
from djstarter.clients import Http2Client
from ua_parser import user_agent_parser
from .const import Ciphers

logger = logging.getLogger(__name__)


class DesktopClient(ABC, Http2Client):
    def __init__(self, fingerprint, *args, **kwargs):
        self.fingerprint = fingerprint
        self.tls_fingerprint = self.fingerprint.tls_fingerprint
        self.user_agent = fingerprint.user_agent
        self.proxies = self.init_proxies()
        super().__init__(proxies=self.proxies, verify=self.new_ssl_context(), *args, **kwargs)

    def send(self, *args, **kwargs):
        self.headers.pop('Accept-Encoding', None)
        self.headers.pop('Connection', None)
        return super().send(*args, **kwargs)

    def new_ssl_context(self):
        context = httpx.create_ssl_context(http2=True)
        context.minimum_version = TLSVersion.TLSv1_2
        context.set_ciphers(self.tls_fingerprint.ciphers)
        context.options = self.tls_fingerprint.extensions

        return context

    def init_proxies(self):
        if proxy := self.fingerprint.proxy:
            return {
                'http://': proxy.http_url,
                'https://': proxy.https_url
            }
        return dict()


class DesktopChromeClient(DesktopClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def sec_ch_ua(self):
        version = UserAgentParser(self.user_agent).browser_major_version
        return f'" Not;A Brand";v="99", "Google Chrome";v="{version}", "Chromium";v="{version}"'

    @property
    def sec_ch_ua_mobile(self):
        return '?0'

    @property
    def sec_ch_ua_platform(self):
        platform = UserAgentParser(self.user_agent).platform
        return f'"{platform}"'


class DesktopFirefoxClient(DesktopClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
