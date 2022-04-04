import logging
from abc import ABC
from ssl import TLSVersion

import httpx
from djstarter.clients import Http2Client
from intoli.models import Profile
from .models import Fingerprint, TLSFingerprint

from . import utils

logger = logging.getLogger(__name__)


class DesktopClient(ABC, Http2Client):
    def __init__(self, fingerprint=None, *args, **kwargs):
        self.fingerprint = fingerprint or self.temp_fingerprint()
        self.tls_fingerprint = self.fingerprint.tls_fingerprint
        self.user_agent = self.fingerprint.user_agent
        super().__init__(
            proxies=self.proxies,
            verify=self.new_ssl_context(),
            *args,
            **kwargs
        )

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

    @property
    def proxies(self):
        if proxy := self.fingerprint.proxy:
            return {
                'http://': proxy.http_url,
                'https://': proxy.https_url
            }
        return dict()

    @staticmethod
    def temp_fingerprint():
        profile = Profile.objects.random_desktop_profile()
        fingerprint = Fingerprint.objects.create(
            device_category=profile.device_category,
            platform=profile.platform,
            screen_height=profile.screen_height,
            screen_width=profile.screen_width,
            user_agent=profile.user_agent,
            viewport_height=profile.viewport_height,
            viewport_width=profile.viewport_width,
        )
        TLSFingerprint.objects.create(
            fingerprint=fingerprint
        )
        return fingerprint


class DesktopChromeClient(DesktopClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ua_parser = utils.UserAgentParser(self.user_agent)

    def init_headers(self):
        return {
            'user-agent': self.user_agent,
        }

    @property
    def sec_ch_ua(self):
        version = self.ua_parser.browser_major_version
        return f'" Not;A Brand";v="99", "Google Chrome";v="{version}", "Chromium";v="{version}"'

    @property
    def sec_ch_ua_mobile(self):
        return '?0'

    @property
    def sec_ch_ua_platform(self):
        platform = self.ua_parser.os
        return f'"{platform}"'


class DesktopFirefoxClient(DesktopClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_headers(self):
        return {
            'User-Agent': self.user_agent,
        }
