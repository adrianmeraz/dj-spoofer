import logging

from djstarter import decorators

from .exceptions import IncolumitasError

logger = logging.getLogger(__name__)

BASE_URL = 'https://api.incolumitas.com'


@decorators.wrap_exceptions(raise_as=IncolumitasError)
def get_ip_fingerprint(client, ip_addr=None):
    url = f'{BASE_URL}/datacenter'

    params = dict()

    if ip_addr:
        params['ip'] = ip_addr

    r = client.get(url, params=params)
    r.raise_for_status()
    return r.json()
