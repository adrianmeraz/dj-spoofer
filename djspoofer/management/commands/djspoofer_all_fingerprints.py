from django.conf import settings
from django.core.management.base import BaseCommand
from djstarter import utils

from djspoofer.clients import DesktopChromeClient
from djspoofer.remote.incolumitas import incolumitas_api, incolumitas_tcpip_api, incolumitas_tls_api
from djspoofer.remote.ja3er import ja3er_api
from djspoofer.remote.howsmyssl import howsmyssl_api
from djspoofer.remote.proxyrack import utils as pr_utils


class Command(BaseCommand):
    help = 'Get IP Fingerprint'

    def add_arguments(self, parser):
        parser.add_argument(
            "--proxy-url",
            required=True,
            type=str,
            help="Set the proxy url",
        )
        parser.add_argument(
            "--proxy-args",
            required=False,
            nargs='*',
            help="Set the proxy password",
        )

    def handle(self, *args, **kwargs):
        proxy_http_url = self.proxy_http_url(proxy_url=kwargs['proxy_url'], proxy_args=kwargs.get('proxy_args', list()))
        try:
            with DesktopChromeClient(proxy_url=proxy_http_url) as client:
                self.show_ja3er_details(client)
                self.show_ssl_check(client)
                self.show_ip_fingerprint(client)
                self.show_tcpip_fingerprint(client)
                self.show_tls_fingerprint(client)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error while running command:\n{str(e)}'))
            raise e
        else:
            self.stdout.write(self.style.MIGRATE_LABEL('Finished getting All Fingerprints'))

    def proxy_http_url(self, proxy_url, proxy_args):
        proxy_builder = pr_utils.ProxyBuilder(
            netloc=proxy_url,
            password=settings.PROXY_PASSWORD,
            username=settings.PROXY_USERNAME,
            **self.proxy_options(proxy_args),
        )
        return proxy_builder.http_url

    def show_ip_fingerprint(self, client):
        r_tls = incolumitas_api.get_ip_fingerprint(client)
        self.stdout.write(utils.eye_catcher_line('IP Fingerprint'))
        self.stdout.write(utils.pretty_dict(r_tls))

    def show_tcpip_fingerprint(self, client):
        r_tcpip = incolumitas_tcpip_api.get_tcpip_fingerprint(client)
        self.stdout.write(utils.eye_catcher_line('TCP/IP Fingerprint'))
        self.stdout.write(utils.pretty_dict(r_tcpip))

    def show_tls_fingerprint(self, client):
        r_tls = incolumitas_tls_api.fps(client)
        self.stdout.write(utils.eye_catcher_line('TLS Fingerprint'))
        self.stdout.write(utils.pretty_dict(r_tls))

    def show_ja3er_details(self, client):
        r_json = ja3er_api.get_json(client)
        self.stdout.write(utils.eye_catcher_line('JA3 Details'))
        self.stdout.write(utils.pretty_dict(r_json))

        r_search = ja3er_api.search(client, ja3_hash=r_json.ja3_hash)
        self.stdout.write(utils.eye_catcher_line('JA3 Hash Search'))
        self.stdout.write(utils.pretty_dict(r_search.json()))

    def show_ssl_check(self, client):
        r_check = howsmyssl_api.ssl_check(client)
        self.stdout.write(utils.eye_catcher_line('SSL Check'))
        self.stdout.write(utils.pretty_dict(r_check.data))

    @staticmethod
    def proxy_options(proxy_args):
        return {args.split('=')[0]: args.split('=')[1] for args in proxy_args}