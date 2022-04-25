import logging
from ssl import TLSVersion

import httpx
from djstarter.clients import Http2Client

from djspoofer import utils
from djspoofer.remote.proxyrack import backends
from .models import Geolocation, Fingerprint

logger = logging.getLogger(__name__)


class DesktopClient(Http2Client, backends.ProxyRackProxyBackend):
    def __init__(self, fingerprint, *args, **kwargs):
        self.fingerprint = fingerprint
        super().__init__(
            proxies=self._proxies,
            verify=self._new_ssl_context(),
            *args,
            **kwargs
        )

    @property
    def _proxies(self):
        proxy_url = self.get_proxy_url(self._get_ip_fingerprint())
        return utils.proxy_dict(proxy_url)

    def send(self, *args, **kwargs):
        self.headers.pop('Accept-Encoding', None)
        self.headers.pop('Connection', None)
        return super().send(*args, **kwargs)

    def _new_ssl_context(self):
        tls_fingerprint = self.fingerprint.tls_fingerprint

        context = httpx.create_ssl_context(http2=True)
        context.minimum_version = TLSVersion.TLSv1_2
        context.set_ciphers(tls_fingerprint.ciphers)
        context.options = tls_fingerprint.extensions

        return context

    def _get_ip_fingerprint(self):
        ip_fingerprints = Fingerprint.objects.get_n_ip_fingerprints(oid=self.fingerprint.oid, count=3)
        if ip_fingerprint := self._get_valid_ip_fingerprint(ip_fingerprints):
            if not self.fingerprint.geolocation:
                self._set_fingerprint_geolocation(self.fingerprint, ip_fingerprint=ip_fingerprint)
            return ip_fingerprint   # Valid IP Fingerprint was found
        return self.new_ip_fingerprint(self.fingerprint)   # Generate if no valid IP Fingerprints

    @staticmethod
    def _set_fingerprint_geolocation(fingerprint, ip_fingerprint):
        geolocation = Geolocation.objects.create(
            city=ip_fingerprint.city,
            country=ip_fingerprint.country,
            isp=ip_fingerprint.isp,
        )
        fingerprint.set_geolocation(geolocation)
        logger.info(f'Set new geolocation for fingerprint: {fingerprint.oid}')

    def _get_valid_ip_fingerprint(self, ip_fingerprints):
        for ip_fp in ip_fingerprints:
            proxy_url = self.get_proxy_url(ip_fingerprint=ip_fp)
            if self.is_valid_proxy(proxies=utils.proxy_dict(proxy_url)):
                return ip_fp
        return None


class DesktopChromeClient(DesktopClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ua_parser = utils.UserAgentParser(self.fingerprint.user_agent)

    def init_headers(self):
        return {
            'user-agent': self.fingerprint.user_agent,
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
            'User-Agent': self.fingerprint.user_agent,
        }
