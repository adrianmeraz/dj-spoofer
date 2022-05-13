from django.core.management.base import BaseCommand
from httpx import Client

from djspoofer.clients import DesktopChromeClient


class Command(BaseCommand):
    help = 'Test Proxies'

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            required=True,
            type=str,
            help="Target URL for proxies",
        )
        parser.add_argument(
            "--proxy-enabled",
            required=False,
            type=bool,
            default=True,
            help="Proxy Enabled",
        )

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        try:
            with DesktopChromeClient(proxy_enabled=kwargs.get('proxy_enabled', True)) as client:
                client.get(url)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successful GET for "{url}"'))
