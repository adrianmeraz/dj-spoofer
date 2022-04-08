import uuid

from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer import const


class Command(BaseCommand):
    help = 'Generate Proxy CSV'

    PROXY_FIELDS = ['oid', 'url', 'mode', 'country', 'city']

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            type=str,
            help="Target URL for proxies",
        )

        parser.add_argument(
            "--port-start",
            required=True,
            type=int,
            help="Proxy port start range",
        )
        parser.add_argument(
            "--port-end",
            required=True,
            type=int,
            help="Proxy port end range",
        )
        parser.add_argument(
            "--credentials",
            type=str,
            help="Proxy credentials",
        )
        parser.add_argument(
            "--proxy-mode",
            default=const.ProxyModes.STICKY.value,
            type=int,
            help="Proxy Mode",
        )

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        port_start = kwargs['port_start']
        port_end = kwargs['port_end']
        proxy_mode = kwargs['proxy_mode']
        credentials = kwargs['credentials']

        self.stdout.write(self.style.MIGRATE_LABEL(','.join(self.PROXY_FIELDS)))
        try:
            for port in range(port_start, port_end):
                columns = [
                    str(uuid.uuid4()),
                    self.build_proxy_str(url, port=port, credentials=credentials),
                    str(proxy_mode),
                    '',
                    ''
                ]
                self.stdout.write(self.style.MIGRATE_LABEL(','.join(columns)))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(utils.eye_catcher_line('Successfully generated proxy csv')))

    @staticmethod
    def build_proxy_str(url, port, credentials=None):
        proxy_str = f'{url}:{port}'
        if credentials:
            proxy_str = f'{credentials}@{proxy_str}'
        return proxy_str
