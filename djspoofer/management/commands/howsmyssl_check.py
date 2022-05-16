from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer import clients
from djspoofer.remote.howsmyssl import howsmyssl_api


class Command(BaseCommand):
    help = 'SSL Check'

    def handle(self, *args, **kwargs):
        try:
            with clients.desktop_client() as client:
                r_check = howsmyssl_api.ssl_check(client)
                self.stdout.write(utils.pretty_dict(r_check))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully got ssl check details'))
