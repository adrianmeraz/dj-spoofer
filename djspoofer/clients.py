import logging

from djstarter import decorators
from httpx import Client, Timeout, TransportError

from djspoofer.models import Profile

logger = logging.getLogger(__name__)

TIMEOUT = Timeout(connect=5, read=10, write=5, pool=5)
RETRY_EXCEPTIONS = (
    TransportError
)


class SpoofedDesktopSession(Client):
    def __init__(self, proxy_url=None, user_agent=None):
        self.proxies = {
            'http://': f'http://{proxy_url}/',
            'https://': f'https://{proxy_url}/'
        }
        self.user_agent = user_agent or Profile.objects.weighted_desktop_profile().user_agent
        self.headers = {
            'user-agent': self.user_agent
        }
        super().__init__(proxies=self.proxies, headers=self.headers)

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
