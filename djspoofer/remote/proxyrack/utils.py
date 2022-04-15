class ProxyBuilder:
    def __init__(self, username, password, netloc, **options):
        self._username = username
        self._password = password
        self._netloc = netloc
        self._options = options

    @property
    def http_url(self):
        return f'http://{self._all_options}:{self._password}@{self._netloc}'

    @property
    def _all_options(self):
        return ';'.join([self._username] + [f'{k}={v}' for k, v in self._options.items()])
