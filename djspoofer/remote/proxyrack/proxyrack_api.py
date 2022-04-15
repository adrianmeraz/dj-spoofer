import logging

from djstarter import decorators

from .exceptions import ProxyRackError

logger = logging.getLogger(__name__)

BASE_URL = 'https://api.proxyrack.net'


@decorators.wrap_exceptions(raise_as=ProxyRackError)
def active_connections(client, *args, **kwargs):
    url = f'{BASE_URL}/active_conns'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return ActiveConnectionsResponse(r.json())


class ActiveConnectionsResponse:
    class Connection:
        def __init__(self, data):
            self.create_time = data['create_time']
            self.dest_addr = data['dest_addr']
            self.source_addr = data['sourceAddr']

    def __init__(self, data):
        self.connections = [self.Connection(c) for c in data]


@decorators.wrap_exceptions(raise_as=ProxyRackError)
def cities(client, *args, **kwargs):
    url = f'{BASE_URL}/cities'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return r.json()


@decorators.wrap_exceptions(raise_as=ProxyRackError)
def countries(client, *args, **kwargs):
    url = f'{BASE_URL}/countries'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return r.json()


@decorators.wrap_exceptions(raise_as=ProxyRackError)
def isps(client, country, *args, **kwargs):
    url = f'{BASE_URL}/countries/{country}/isps'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return r.json()


@decorators.wrap_exceptions(raise_as=ProxyRackError)
def ip_count(client, country, *args, **kwargs):
    url = f'{BASE_URL}/countries/{country}/count'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return r.json()


@decorators.wrap_exceptions(raise_as=ProxyRackError)
def generate_temp_api_key(client, expiration_seconds, *args, **kwargs):
    url = f'{BASE_URL}/passwords'

    params = {
        'expirationSeconds': expiration_seconds,
    }

    r = client.get(url, params=params, *args, **kwargs)
    r.raise_for_status()
    return ActiveConnectionsResponse(r.json())


class GenerateTempApiKeyResponse:
    class Password:
        def __init__(self, data):
            self.expiration_seconds = data['expirationSeconds']
            self.password = data['password']

    def __init__(self, data):
        self.password = self.Password(data['password'])
        self.success = data['success']


@decorators.wrap_exceptions(raise_as=ProxyRackError)
def stats(client, *args, **kwargs):
    url = f'{BASE_URL}/stats'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return StatsResponse(r.json())


class StatsResponse:
    class IPInfo:
        class Fingerprint:
            def __init__(self, data):
                self.osName = data['osName']

        def __init__(self, data):
            self.city = data['expirationSeconds']
            self.country = data['password']
            self.fingerprint = self.Fingerprint(data['fingerprint'])
            self.ip = data['ip']
            self.isp = data['isp']
            self.online = data['online']
            self.proxyId = data['proxyId']

    def __init__(self, data):
        self.ipinfo = self.IPInfo(data['ipinfo'])
