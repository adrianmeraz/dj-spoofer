from django.core.management.base import BaseCommand

from djspoofer.models import Fingerprint, DeviceFingerprint, TLSFingerprint
from djspoofer import utils
from djspoofer.models import IntoliFingerprint


class Command(BaseCommand):
    help = 'Create Desktop Fingerprints'

    def add_arguments(self, parser):
        parser.add_argument(
            "--num_to_create",
            required=True,
            type=int,
            help="Number of Fingerprints to Create",
        )

    def handle(self, *args, **kwargs):
        try:
            self.create_all_fingerprints(kwargs['num_to_create'])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully created fingerprints'))

    def create_all_fingerprints(self, num_to_create):
        fingerprints = list()
        for _ in range(num_to_create):
            fingerprints.append(self.create_fingerprint())
        self.stdout.write(self.style.MIGRATE_LABEL(f'Fingerprints created: {len(fingerprints)}'))

    @staticmethod
    def create_fingerprint():
        profile = IntoliFingerprint.objects.random_desktop()
        ua_parser = utils.UserAgentParser(profile.user_agent)
        return Fingerprint.objects.create(
            device_fingerprint=DeviceFingerprint.objects.create(
                browser=ua_parser.browser,
                browser_major_version=ua_parser.browser_major_version,
                device_category=profile.device_category,
                os=ua_parser.os,
                platform=profile.platform,
                screen_height=profile.screen_height,
                screen_width=profile.screen_width,
                user_agent=profile.user_agent,
                viewport_height=profile.viewport_height,
                viewport_width=profile.viewport_width,
            )
        )
