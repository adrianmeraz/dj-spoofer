import logging
import uuid
from abc import ABC
from ssl import TLSVersion

import httpx
from django.conf import settings
from djstarter.clients import Http2Client

from djspoofer import utils
from djspoofer.remote.proxyrack import exceptions as pr_exceptions, proxyrack_api, utils as pr_utils
from .models import Fingerprint, TLSFingerprint, Proxy

logger = logging.getLogger(__name__)


class ProxyBackend(ABC):

    def ip_fingerprint_proxy_url(self, ip_fingerprint):
        raise NotImplemented

    def is_valid_proxy(self, proxy_url):
        raise NotImplemented


class ProxyRackProxyBackend(ProxyBackend):
    def __init__(self, *args, **kwargs):
        self.proxy = Proxy.objects.get_rotating_proxy()

    def ip_fingerprint_proxy_url(self, ip_fingerprint):
        return self.build_proxy_url(
            country=ip_fingerprint.country,
            city=ip_fingerprint.city,
            isp=ip_fingerprint.isp,
            proxyIp=ip_fingerprint.ip,
            osName=ip_fingerprint.fingerprint.os
        )

    def build_proxy_url(self, **kwargs):
        proxy_builder = pr_utils.ProxyBuilder(
            username=settings.PROXY_USERNAME,
            password=settings.PROXY_PASSWORD,
            netloc=self.proxy.url,
            refreshMinutes=10,
            session=str(uuid.uuid4()),
            **kwargs
        )
        return proxy_builder.http_url

    def is_valid_proxy(self, proxy_url):
        proxies = {
            'http://': proxy_url,
            'https://': proxy_url
        }
        with Http2Client(proxies=proxies) as client:
            try:
                proxyrack_api.proxy_check(client)
            except pr_exceptions.ProxyError:
                return False
            else:
                return True


class DesktopClient(Http2Client, ProxyRackProxyBackend):
    def __init__(self, fingerprint=None, *args, **kwargs):
        self.fingerprint = fingerprint or self.temp_fingerprint()
        self.tls_fingerprint = self.fingerprint.tls_fingerprint or self.generate_tls_fingerprint()
        self.ip_fingerprint = self.get_ip_fingerprint()
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
        proxy_url = self.ip_fingerprint_proxy_url(self.ip_fingerprint)
        if proxy_url:
            return {
                'http://': proxy_url,
                'https://': proxy_url
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
        if ip_fingerprints := Fingerprint.objects.get_n_ip_fingerprints(oid=self.fingerprint.oid, count=3):
            if ip_fingerprint := self.get_valid_ip_fingerprint(ip_fingerprints):      # Valid IP Fingerprint was found
                return ip_fingerprint
            else:                   # IP Fingerprints were invalid. Generate a new one using geolocation
                pass
        else:                       # No Prior IP Fingerprints - Generate an IP Fingerprint
            pass

    def get_valid_ip_fingerprint(self, ip_fingerprints):
        for ip_fp in ip_fingerprints:
            proxy_url = self.ip_fingerprint_proxy_url(ip_fingerprint=ip_fp)
            if self.is_valid_proxy(proxy_url):
                return ip_fp
            else:
                continue
        return None


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
