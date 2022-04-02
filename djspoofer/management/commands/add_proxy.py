from django.core.management.base import BaseCommand

from djspoofer import const
from djspoofer.models import Proxy


class Command(BaseCommand):
    help = 'Add Proxy'

    def add_arguments(self, parser):
        parser.add_argument(
            "--mode",
            choices=const.ProxyModes.labels(),
            required=True,
            type=str,
            help="Sets the proxy mode",
        )
        parser.add_argument(
            "--url",
            required=True,
            type=str,
            help="Set the proxy url",
        )
        parser.add_argument(
            "--country",
            default='',
            type=str,
            help="Set the proxy country",
        )
        parser.add_argument(
            "--city",
            default='',
            type=str,
            help="Set the proxy city",
        )

    def handle(self, *args, **kwargs):
        try:
            proxy = Proxy.objects.create(
                mode=const.ProxyModes.by_label(kwargs['mode']),
                url=kwargs['url'],
                country=kwargs['country'],
                city=kwargs['city'],
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL(f'Created proxy "{proxy.url}"'))
