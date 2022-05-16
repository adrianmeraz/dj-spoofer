import argparse

from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer import clients
from djspoofer.models import Fingerprint
from djspoofer.remote.incolumitas import incolumitas_tls_api


class Command(BaseCommand):
    help = 'Get TLS Fingerprint'

    def add_arguments(self, parser):
        parser.add_argument(
            "--browser",
            type=str,
            required=False,
        )
        parser.add_argument(
            "--proxy-enabled",
            action=argparse.BooleanOptionalAction,
            help="Proxy Enabled",
        )

    def handle(self, *args, **kwargs):
        try:
            fp = Fingerprint.objects.random_desktop(browser=kwargs.get('browser'))
            with clients.desktop_client(fingerprint=fp, proxy_enabled=kwargs['proxy_enabled']) as client:
                r_tls = incolumitas_tls_api.tls_fingerprint(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_tls))
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting TLS Fingerprint'))
