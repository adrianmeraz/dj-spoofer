import argparse

from django.core.management.base import BaseCommand

from djspoofer import clients, exceptions

BROWSER_MAP = {
    'chrome': clients.DesktopChromeClient,
    'firefox': clients.DesktopFirefoxClient
}


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
            with self.get_client_class(browser=kwargs['browser'])(proxy_enabled=proxy_enabled) as client:
                for url in kwargs['urls']:
                    r = client.get(url)
                    if kwargs['display_output']:
                        self.stdout.write(r.text)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successful GET for "{url}"'))

    @staticmethod
    def get_client_class(browser):
        try:
            return BROWSER_MAP[browser]
        except IndexError:
            raise exceptions.DJSpooferError(
                f'Unknown browser: {browser}. Set Browser to one of the following: {BROWSER_MAP.keys()}')
