import logging
import socket
from abc import ABC
from ssl import TLSVersion
from urllib import parse

import httpcore
import httpx
from djstarter.clients import Http2Client
from httpcore._exceptions import (
    ConnectError,
    ConnectTimeout,
    map_exceptions,
)
from httpcore.backends import sync

from . import utils
from .models import Fingerprint, TLSFingerprint

logger = logging.getLogger(__name__)


class TcpipBackend(sync.SyncBackend):
    def connect_tcp(self, host, port, timeout=10, local_address=None):
        address = (host, port)
        source_address = None if local_address is None else (local_address, 0)
        exc_map = {socket.timeout: ConnectTimeout, socket.error: ConnectError}
        with map_exceptions(exc_map):
            sock = self.create_connection(address, timeout, source_address=source_address)
        return sync.SyncStream(sock)

    # def create_socket(self, timeout, path):
    #     exc_map = {socket.timeout: ConnectTimeout, socket.error: ConnectError}
    #     with map_exceptions(exc_map):
    #         sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    #         sock.settimeout(timeout)
    #         sock.connect(path)

    def create_connection(self, address, timeout=10, source_address=None):
        """Connect to *address* and return the socket object.

        Convenience function.  Connect to *address* (a 2-tuple ``(host,
        port)``) and return the socket object.  Passing the optional
        *timeout* parameter will set the timeout on the socket instance
        before attempting to connect.  If no *timeout* is supplied, the
        global default timeout setting returned by :func:`getdefaulttimeout`
        is used.  If *source_address* is set it must be a tuple of (host, port)
        for the socket to bind as a source address before making the connection.
        A host of '' or port 0 tells the OS to use the default.
        """

        host, port = address
        err = None
        for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            sock = None
            try:
                sock = socket.socket(af, socktype, proto)
                self.set_socket_flags(sock)
                sock.settimeout(timeout)
                if source_address:
                    sock.bind(source_address)
                sock.connect(sa)
                # Break explicitly a reference cycle
                err = None
                return sock

            except socket.error as _:
                err = _
                if sock is not None:
                    sock.close()

        if err is not None:
            try:
                raise err
            finally:
                # Break explicitly a reference cycle
                err = None
        else:
            raise socket.error("getaddrinfo returns an empty list")

    @staticmethod
    def set_socket_flags(sock):
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_MAXSEG, 1460)    # (tcp_mss) Max Segment Size
        # Can't get exact Window Scaling Values, so will leave this for now
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64240)  # (tcp_window_size) - Max 65535
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, 64)              # (ip_ttl) - Max 255


class GenericConnectionPool(httpcore.ConnectionPool):
    class Response(httpcore.Response):
        pass

    def get(self, url, params=None, *args, **kwargs):
        if params:
            url += f'?{parse.urlencode(params)}'
        return self.request('GET', url, *args, **kwargs)


class ProxyConnectionPool(httpcore.HTTPProxy):
    class Response(httpcore.Response):
        pass

    def get(self, url, params=None, *args, **kwargs):
        if params:
            url += f'?{parse.urlencode(params)}'
        return self.request('GET', url, *args, **kwargs)


class DesktopConnectionPool(GenericConnectionPool):
    def __init__(self, fingerprint=None, proxy=None, *args, **kwargs):
        self.fingerprint = fingerprint or self.temp_fingerprint()
        self.tls_fingerprint = self.fingerprint.tls_fingerprint or self.generate_tls_fingerprint()
        self.proxy = proxy
        self.user_agent = self.fingerprint.user_agent
        super().__init__(
            network_backend=TcpipBackend(),
            # proxy_url=self.proxy_url,
            # proxy_auth=self.proxy_auth,
            ssl_context=self.new_ssl_context(),
            *args,
            **kwargs
        )

    @staticmethod
    def temp_fingerprint():
        return Fingerprint.objects.get_random_desktop_fingerprint()

    def generate_tls_fingerprint(self):
        tls_fingerprint = TLSFingerprint.objects.create(browser=self.fingerprint.browser)
        self.fingerprint.tls_fingerprint = tls_fingerprint
        self.fingerprint.save()
        return tls_fingerprint

    @property
    def proxy_url(self):
        return self.proxy.http_url if self.proxy else None

    @property
    def proxy_auth(self):
        return (self.proxy.auth_username, self.proxy.auth_password) if self.proxy else None

    def new_ssl_context(self):
        context = httpx.create_ssl_context(http2=True)
        context.minimum_version = TLSVersion.TLSv1_2
        context.set_ciphers(self.tls_fingerprint.ciphers)
        context.options = self.tls_fingerprint.extensions

        return context


class DesktopClient(ABC, Http2Client):
    def __init__(self, fingerprint=None, proxy=None, *args, **kwargs):
        self.fingerprint = fingerprint or self.temp_fingerprint()
        self.proxy = proxy
        self.tls_fingerprint = self.fingerprint.tls_fingerprint or self.generate_tls_fingerprint()
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
        if self.proxy:
            return {
                'http://': self.proxy.http_url,
                'https://': self.proxy.http_url
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
