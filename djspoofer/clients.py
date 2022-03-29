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
    CIPHERS = [
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
    ]

    TLS_EXTENSIONS = (
        Options.OP_NO_SSLv2,
        Options.OP_NO_SSLv3,
        Options.OP_NO_TLSv1,
        Options.OP_NO_TLSv1_1,
        Options.OP_CIPHER_SERVER_PREFERENCE,
        Options.OP_SINGLE_DH_USE,
        Options.OP_SINGLE_ECDH_USE,
        Options.OP_NO_COMPRESSION,
        Options.OP_NO_TICKET,
        Options.OP_NO_RENEGOTIATION,
        Options.OP_ENABLE_MIDDLEBOX_COMPAT,
    )

    def __init__(self, fingerprint, *args, **kwargs):
        self.fingerprint = fingerprint
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
        context.set_ciphers(self.cipher_string)
        context.options = self.random_tls_extension_int()

        return context

    def shuffled_ciphers(self, start_idx=0, min_k=6):
        first_ciphers = self.CIPHERS[:start_idx]
        rem_ciphers = self.CIPHERS[start_idx:]
        k = random.randint(min_k, len(rem_ciphers))
        return first_ciphers + random.sample(rem_ciphers, k=k)

    def init_proxies(self):
        if proxy := self.fingerprint.proxy:
            return {
                'http://': proxy.http_url,
                'https://': proxy.https_url
            }
        return dict()

    def random_tls_extension_int(self, min_k=4):
        k = random.randint(min_k, len(self.TLS_EXTENSIONS))
        ext_val = 0
        for ext in random.sample(self.TLS_EXTENSIONS, k=k):
            ext_val |= ext
        return ext_val

    @property
    def cipher_string(self):
        raise NotImplemented


class DesktopChromeClient(DesktopClient):

    CIPHERS = [
        Ciphers.TLS_GREASE,
        Ciphers.TLS_AES_128_GCM_SHA256,
        Ciphers.TLS_AES_256_GCM_SHA384,
        Ciphers.TLS_CHACHA20_POLY1305_SHA256,
        Ciphers.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
        Ciphers.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
        Ciphers.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
        Ciphers.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
        Ciphers.TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,
        Ciphers.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,
        Ciphers.TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,
        Ciphers.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,
        Ciphers.TLS_RSA_WITH_AES_128_GCM_SHA256,
        Ciphers.TLS_RSA_WITH_AES_256_GCM_SHA384,
        Ciphers.TLS_RSA_WITH_AES_128_CBC_SHA,
        Ciphers.TLS_RSA_WITH_AES_256_CBC_SHA,
    ]

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

    @property
    def cipher_string(self):
        return ':'.join([c.value for c in self.shuffled_ciphers(start_idx=4)])


class DesktopFirefoxClient(DesktopClient):
    CIPHERS = [
        Ciphers.TLS_AES_128_GCM_SHA256,
        Ciphers.TLS_CHACHA20_POLY1305_SHA256,
        Ciphers.TLS_AES_256_GCM_SHA384,
        Ciphers.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
        Ciphers.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
        Ciphers.TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,
        Ciphers.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,
        Ciphers.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
        Ciphers.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
        Ciphers.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
        Ciphers.TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,
        Ciphers.TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,
        Ciphers.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,
        Ciphers.TLS_RSA_WITH_AES_128_GCM_SHA256,
        Ciphers.TLS_RSA_WITH_AES_256_GCM_SHA384,
        Ciphers.TLS_RSA_WITH_AES_128_CBC_SHA,
        Ciphers.TLS_RSA_WITH_AES_256_CBC_SHA,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def cipher_string(self):
        return ':'.join([c.value for c in self.shuffled_ciphers(start_idx=3)])


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
