from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer.clients import DesktopChromeClient
from djspoofer.remote.ja3er import ja3er_api


class Command(BaseCommand):
    help = 'Ja3er Check'

    def handle(self, *args, **kwargs):
        try:
            with DesktopChromeClient() as chrome_client:
                self.show_ja3er_details(chrome_client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully got ja3er details'))

    def show_ja3er_details(self, client):
        r_json = ja3er_api.details(client)
        self.stdout.write(utils.eye_catcher_line('JA3 Details'))
        self.stdout.write(utils.pretty_dict(r_json))

        r_search = ja3er_api.search(client, ja3_hash=r_json.ja3_hash)
        self.stdout.write(utils.eye_catcher_line('JA3 Hash Search'))
        self.stdout.write(utils.pretty_dict(vars(r_search)))



