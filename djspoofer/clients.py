import logging

from djstarter import decorators
from httpx import Client, Timeout, TransportError

from djspoofer.models import Fingerprint

logger = logging.getLogger(__name__)

TIMEOUT = Timeout(connect=5, read=10, write=5, pool=5)
RETRY_EXCEPTIONS = (
    TransportError
)


class SpoofedDesktopClient(Client):
    def __init__(self, fingerprint):
        self.fingerprint = fingerprint
        self.proxies = {
            'http://': f'http://{fingerprint.proxy}',
            'https://': f'https://{fingerprint.proxy}'
        }
        self.headers = {
            'user-agent': self.fingerprint.user_agent
        }
        super().__init__(headers=self.headers, proxies=self.proxies, timeout=TIMEOUT)

    @decorators.retry(retry_exceptions=RETRY_EXCEPTIONS)
    @decorators.api_error_check
    def send(self, *args, **kwargs):
        return super().send(*args, **kwargs)


class SpooferClient(Client):
    """
    Spoofer Http Client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(headers=self.get_headers(), timeout=TIMEOUT, *args, **kwargs)

    @staticmethod
    def get_headers():
        return {
            'accept': 'application/json',
        }

    @decorators.retry(retry_exceptions=RETRY_EXCEPTIONS)
    @decorators.api_error_check
    def send(self, *args, **kwargs):
        return super().send(*args, **kwargs)
