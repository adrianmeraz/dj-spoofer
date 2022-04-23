import logging
from abc import ABC
from ssl import TLSVersion

import httpx
from djstarter.clients import Http2Client

from djspoofer import utils
import uuid
from django.conf import settings
from djspoofer.remote.proxyrack import exceptions, proxyrack_api, utils as pr_utils
from .models import Fingerprint, IPFingerprint, TLSFingerprint, Proxy

logger = logging.getLogger(__name__)


class ProxyRackProxyBackend:
    @staticmethod
    def build_proxy_url(netloc, **kwargs):
        proxy_builder = pr_utils.ProxyBuilder(
            username=settings.PROXY_USERNAME,
            password=settings.PROXY_PASSWORD,
            netloc=netloc,
            country=kwargs.get('countries'),
            city=kwargs.get('cities'),
            isp=kwargs.get('isps'),
            refreshMinutes=10,
            osName=kwargs.get('os_name'),
            session=str(uuid.uuid4()),
            proxyIp=kwargs.get('proxy_ip'),
        )
        return proxy_builder.http_url


class DesktopClient(ABC, Http2Client, ProxyRackProxyBackend):
    def __init__(self, fingerprint=None, *args, **kwargs):
        self.fingerprint = fingerprint or self.temp_fingerprint()
        self.tls_fingerprint = self.fingerprint.tls_fingerprint or self.generate_tls_fingerprint()
        self.user_agent = self.fingerprint.user_agent
        self.proxy_url = None
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
        if self.proxy_url:
            return {
                'http://': self.proxy_url,
                'https://': self.proxy_url
            }
        return dict()

    @staticmethod
    def temp_fingerprint():
        return Fingerprint.objects.get_random_desktop_fingerprint()

    def generate_tls_fingerprint(self):
        tls_fingerprint = TLSFingerprint.objects.create(browser=self.fingerprint.browser)
        self.fingerprint.tls_fingerprint = tls_fingerprint
        self.fingerprint.save()
        return tls_fingerprint

    def get_ip_fingerprint(self):
        ip_fingerprints = Fingerprint.objects.get_n_ip_fingerprints(oid=self.fingerprint.oid, count=3)
        if self.contains_valid_ip_fingerprint(ip_fingerprints):
            pass
        else:                       # No IP Fingerprints have worked
            if ip_fingerprints:     # There were IP fingerprints
                pass
            else:                   # There were IP fingerprints
                pass

    def contains_valid_ip_fingerprint(self, ip_fingerprints):
        for ip_fp in ip_fingerprints:
            proxy_url = self.generate_proxy_url()
            if self.is_valid_proxy(proxy_url):
                return True
            else:
                continue
        return False

    def generate_proxy_url(self, **kwargs):
        proxy = Proxy.objects.get_rotating_proxy()
        return self.build_proxy_url(netloc=proxy.url, **kwargs)

    def is_valid_proxy(self, proxy_url):
        proxies = {
            'http://': proxy_url,
            'https://': proxy_url
        }
        with Http2Client(proxies=proxies) as client:
            try:
                utils.is_valid_proxy(client)
            except (httpx.HTTPStatusError, httpx.ProxyError):
                return False
            else:
                return True


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
