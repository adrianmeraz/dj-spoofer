from django.core.management.base import BaseCommand
from djstarter import utils

from django.conf import settings
from djspoofer.clients import DesktopChromeClient
from incolumitas import incolumitas_tcpip_api
from proxyrack import utils as pr_utils


class Command(BaseCommand):
    help = 'Get TCP/IP Fingerprint'

    def add_arguments(self, parser):
        parser.add_argument(
            "--proxy-url",
            required=True,
            type=str,
            help="Set the proxy url",
        )
        parser.add_argument(
            "--proxy-args",
            required=False,
            nargs='*',
            help="Set the proxy password",
        )

    def handle(self, *args, **kwargs):
        proxy_builder = pr_utils.ProxyBuilder(
            netloc=kwargs.pop('proxy_url'),
            password=settings.PROXY_PASSWORD,
            username=settings.PROXY_USERNAME,
            **self.proxy_kwargs(kwargs.get('proxy_args', list())),
        )
        try:
            with DesktopChromeClient(proxy_url=proxy_builder.http_url) as client:
                r_tls = incolumitas_tcpip_api.get_tcpip_fingerprint(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_tls))
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting TCP/IP Fingerprint'))

    @staticmethod
    def proxy_kwargs(proxy_args):
        return {args.split('=')[0]: args.split('=')[1] for args in proxy_args}
