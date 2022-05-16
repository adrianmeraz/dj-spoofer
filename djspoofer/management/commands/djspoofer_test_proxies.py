import argparse

from django.core.management.base import BaseCommand

from djspoofer import clients
from djspoofer.models import Fingerprint


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
        parser.add_argument(
            "--browser",
            type=str,
            required=False,
            default='chrome'
        )

    def handle(self, *args, **kwargs):
        proxy_enabled = kwargs['proxy_enabled']
        self.stdout.write(self.style.MIGRATE_LABEL(f'Proxy enabled: {proxy_enabled}'))
        try:
            fp = Fingerprint.objects.random_desktop(browser=kwargs.get('browser'))
            with clients.desktop_client(fingerprint=fp, proxy_enabled=proxy_enabled) as client:
            # with clients.desktop_client(proxy_enabled=proxy_enabled) as client:
                for url in kwargs['urls']:
                    r = client.get(url)
                    if kwargs['display_output']:
                        self.stdout.write(r.text)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successful GET for "{url}"'))
