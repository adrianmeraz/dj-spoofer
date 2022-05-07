from django.core.management.base import BaseCommand

from djspoofer.models import Proxy, Fingerprint, H2Fingerprint, IntoliFingerprint


class Command(BaseCommand):
    help = 'DJ Spoofer Reset'

    def handle(self, *args, **kwargs):
        try:
            self.delete_h2_fingerprints()
            self.delete_proxies()
            self.delete_intoli_fingerprints()
            self.delete_fingerprints()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Reset DJ Spoofer'))

    def delete_h2_fingerprints(self):
        deleted = H2Fingerprint.objects.all().delete()
        self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Deleted {deleted} H2 Fingerprints'))

    def delete_proxies(self):
        deleted = Proxy.objects.all().delete()
        self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Deleted {deleted} Proxies'))

    def delete_intoli_fingerprints(self):
        deleted = IntoliFingerprint.objects.all().delete()
        self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Deleted {deleted} Intoli Fingerprints'))

    def delete_fingerprints(self):
        deleted = Fingerprint.objects.all().delete()
        self.stdout.write(self.style.MIGRATE_LABEL(f'Successfully Deleted {deleted} Fingerprints'))
