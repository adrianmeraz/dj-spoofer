from django.core.management.base import BaseCommand
from httpx import Client
import argparse

from djspoofer.clients import DesktopChromeClient


class Command(BaseCommand):
    help = 'Test Proxies'

    def add_arguments(self, parser):
        parser.add_argument(
            "--urls",
            required=True,
            nargs='*',
            help="Target URLs for proxies",
        )
        parser.add_argument(
            "--proxy-enabled",
            action=argparse.BooleanOptionalAction,
            help="Proxy Enabled",
        )
        parser.add_argument(
            "--display-output",
            action=argparse.BooleanOptionalAction,
            help="Display Output",
        )

    def handle(self, *args, **kwargs):
        urls = kwargs['urls']
        proxy_enabled = kwargs['proxy_enabled']
        self.stdout.write(self.style.MIGRATE_LABEL(f'Proxy enabled: {proxy_enabled}'))
        try:
            with DesktopChromeClient(proxy_enabled=proxy_enabled) as client:
                for url in urls:
                    r = client.get(url)
                    if kwargs['display_output']:
                        self.stdout.write(r.text)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successful GET for "{url}"'))
