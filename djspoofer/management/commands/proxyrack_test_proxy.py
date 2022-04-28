from django.core.management.base import BaseCommand
from djstarter.clients import Http2Client
from httpx import Client
from djspoofer.remote.proxyrack import proxyrack_api

from djspoofer.models import Proxy


class Command(BaseCommand):
    help = 'Test Proxies'

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
        try:
            if kwargs['no_proxies']:
                with Client() as client:
                    client.get(url)
            else:
                with Http2Client(proxy_str=Proxy.objects.get_rotating_proxy().url) as client:
                    client.get(url)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successful GET for "{url}"'))
