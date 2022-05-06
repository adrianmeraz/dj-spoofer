from django.core.management.base import BaseCommand

from djspoofer.models import H2Fingerprint
from djspoofer import utils


class Command(BaseCommand):
    help = 'Save H2 Hash'

    def add_arguments(self, parser):
        parser.add_argument(
            "--hash",
            required=True,
            type=str,
            help="H2 Fingerprint Hash",
        )
        parser.add_argument(
            "--user-agent",
            required=True,
            type=str,
            help="User Agent",
        )
        parser.add_argument(
            "--browser-min-major-version",
            required=False,
            type=int,
            help="Browser Minimum Major Version",
        )
        parser.add_argument(
            "--browser-max-major-version",
            required=False,
            type=int,
            help="Browser Minimum Major Version",
        )

    def handle(self, *args, **kwargs):
        try:
            h2_fingerprint = self.create_h2_fingerprint(kwargs)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully saved H2 Fingerprint: {h2_fingerprint}'))

    @staticmethod
    def create_h2_fingerprint(kwargs):
        ua_parser = utils.UserAgentParser(kwargs['user_agent'])
        h2_parser = utils.H2HashParser(hash=kwargs['hash'])
        return H2Fingerprint.objects.create(
            browser=ua_parser.browser,
            os=ua_parser.os,
            browser_min_major_version=kwargs.get('browser_min_major_version') or ua_parser.browser_major_version,
            browser_max_major_version=kwargs.get('browser_max_major_version') or ua_parser.browser_major_version,
            header_table_size=h2_parser.settings_frame.header_table_size,
            enable_push=bool(h2_parser.settings_frame.push_enabled),
            max_concurrent_streams=h2_parser.settings_frame.max_concurrent_streams,
            initial_window_size=h2_parser.settings_frame.initial_window_size,
            max_frame_size=h2_parser.settings_frame.max_frame_size,
            max_header_list_size=h2_parser.settings_frame.max_header_list_size,
            psuedo_header_order=h2_parser.pseudo_headers,
            window_update_increment=h2_parser.window_frame,
            priority_stream_id=h2_parser.priority_frame.stream_id,
            priority_exclusive=h2_parser.priority_frame.is_exclusive,
            priority_depends_on_id=h2_parser.priority_frame.depends_on_id,
            priority_weight=h2_parser.priority_frame.weight,
        )
