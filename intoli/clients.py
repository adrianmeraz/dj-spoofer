import logging

from djstarter import decorators
from httpx import Client, Timeout, TransportError

logger = logging.getLogger(__name__)

TIMEOUT = Timeout(connect=5, read=10, write=5, pool=5)
RETRY_EXCEPTIONS = (
    TransportError
)


class IntoliClient(Client):
    """
    Intoli Http Client
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


