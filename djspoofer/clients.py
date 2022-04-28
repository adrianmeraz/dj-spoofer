import logging
from ssl import TLSVersion

import httpx
from djstarter.clients import Http2Client

from djspoofer import utils
from djspoofer.remote.proxyrack import backends

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
        return utils.proxy_dict(self.get_proxy_url(self.fingerprint))

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
