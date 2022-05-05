from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer.clients import DesktopChromeClient
from djspoofer.models import Fingerprint, H2Fingerprint
from djspoofer.remote.h2fingerprint import h2fingerprint_api
from djspoofer.utils import H2HashParser


class Command(BaseCommand):
    help = 'Save H2 Hash'

    def add_arguments(self, parser):
        parser.add_argument(
            "--hash",
            required=True,
            type=str,
            help="Set the proxy url",
        )

    def handle(self, *args, **kwargs):
        try:
            h2_parser = H2HashParser(hash=kwargs['hash'])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_h2))
            self.stdout.write(self.style.MIGRATE_LABEL('Successfully saved H2 Fingerprint: {}'))

    def create_h2_fingerprint(self, h2_hash):
        h2_parser = H2HashParser(hash=h2_hash)
        H2Fingerprint.objects.create(

        )
