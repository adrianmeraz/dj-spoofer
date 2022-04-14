from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer.clients import DesktopChromeClient
from djspoofer.models import Proxy
from incolumitas import incolumitas_tcpip_api


class Command(BaseCommand):
    help = 'Get TCP/IP Fingerprint'

    def handle(self, *args, **kwargs):
        try:
            with DesktopChromeClient(proxy=Proxy.objects.get_sticky_proxy()) as client:
                r_tls = incolumitas_tcpip_api.get_tcpip_fingerprint(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(utils.pretty_dict(r_tls))
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting TCP/IP Fingerprint'))
