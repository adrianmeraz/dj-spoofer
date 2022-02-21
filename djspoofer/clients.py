import logging

from djstarter import decorators
from httpx import Client, Timeout, TransportError

logger = logging.getLogger(__name__)

TIMEOUT = Timeout(connect=5, read=10, write=5, pool=5)
RETRY_EXCEPTIONS = (
    TransportError
)


class SpoofedDesktopClient(Client):
    def __init__(self, fingerprint, *args, **kwargs):
        self.fingerprint = fingerprint
        self.proxies = {
            'http://': fingerprint.proxy.http_url,
            'https://': fingerprint.proxy.https_url
        }
        super().__init__(
            follow_redirects=True,
            headers=self.get_headers(),
            http2=True,
            proxies=self.proxies,
            timeout=TIMEOUT,
            *args,
            **kwargs
        )

    @decorators.retry(retry_exceptions=RETRY_EXCEPTIONS)
    @decorators.api_error_check
    def send(self, *args, **kwargs):
        return super().send(*args, **kwargs)

    def get_headers(self):
        return {
            'accept': 'application/json',
            'user-agent': self.fingerprint.user_agent
        }


class SpooferClient(Client):
    """
    Http/2 Client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            follow_redirects=True,
            http2=True,
            headers=self.get_headers(),
            timeout=TIMEOUT,
            *args,
            **kwargs
        )

    @staticmethod
    def get_headers():
        return {
            'accept': 'application/json',
        }

    @decorators.retry(retry_exceptions=RETRY_EXCEPTIONS)
    @decorators.api_error_check
    def send(self, *args, **kwargs):
        return super().send(*args, **kwargs)
