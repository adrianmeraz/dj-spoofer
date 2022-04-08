import logging

from djstarter import decorators

from .exceptions import IncolumitasError

logger = logging.getLogger(__name__)

BASE_URL = 'https://tcpip.incolumitas.com'


@decorators.wrap_exceptions(raise_as=IncolumitasError)
def get_tcpip_fingerprint(client):
    url = f'{BASE_URL}/classify'

    params = {
        'by_ip': '1',
    }

    r = client.get(url, params=params)
    r.raise_for_status()
    return r.json()
