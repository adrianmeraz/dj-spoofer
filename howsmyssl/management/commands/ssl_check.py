from django.core.management.base import BaseCommand

from howsmyssl import howsmyssl_api
from djspoofer.clients import DesktopChromeClient
from djspoofer.models import Fingerprint


class Command(BaseCommand):
    help = 'SSL Check'

    def handle(self, *args, **kwargs):
        try:
            with DesktopChromeClient(self.create_fingerprint()) as chrome_client:
                r_check = howsmyssl_api.ssl_check(chrome_client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully got ssl check details'))

    def create_fingerprint(self):
        return Fingerprint.objects.create(
            device_category='desktop',
            platform='windows',
            screen_height=1080,
            screen_width=1920,
            user_agent='Test User Agent 1.0',
            viewport_height=1080,
            viewport_width=1920,
            # proxy=proxy
        )
