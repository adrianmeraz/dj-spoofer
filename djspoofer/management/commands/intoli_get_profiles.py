from django.core.management.base import BaseCommand
from djspoofer.remote.intoli import tasks


class Command(BaseCommand):
    help = 'Get Intoli Profiles'

    def handle(self, *args, **kwargs):
        try:
            tasks.get_profiles()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting profiles from Intoli'))
