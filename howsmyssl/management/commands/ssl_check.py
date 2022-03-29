from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer.clients import DesktopChromeClient
from djspoofer.models import Fingerprint
from howsmyssl import howsmyssl_api
from intoli.models import Profile


class Command(BaseCommand):
    help = 'SSL Check'

    def handle(self, *args, **kwargs):
        try:
            with DesktopChromeClient(self.get_fingerprint()) as chrome_client:
                r_check = howsmyssl_api.ssl_check(chrome_client)
                self.stdout.write(utils.pretty_dict(r_check.data))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully got ssl check details'))

    @staticmethod
    def get_fingerprint():
        profile = Profile.objects.weighted_desktop_profile()
        return Fingerprint(
            device_category=profile.device_category,
            platform=profile.platform,
            screen_height=profile.screen_height,
            screen_width=profile.screen_width,
            user_agent=profile.user_agent,
            viewport_height=profile.viewport_height,
            viewport_width=profile.viewport_width,
            # proxy=proxy
        )
