import logging

from djstarter import decorators

from .exceptions import IncolumitasError

logger = logging.getLogger(__name__)

BASE_URL = 'https://tls.incolumitas.com'


@decorators.wrap_exceptions(raise_as=IncolumitasError)
def fps(client):
    url = f'{BASE_URL}/fps'

    params = {
        'detail': '1',
    }

    r = client.get(url, params=params)
    r.raise_for_status()
    return r.json()

