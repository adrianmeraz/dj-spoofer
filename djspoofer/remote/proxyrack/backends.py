import logging
import uuid

from django.conf import settings
from djstarter.clients import Http2Client
from httpx import Client

from djspoofer import backends, exceptions, utils
from djspoofer.models import IPFingerprint, Proxy
from djspoofer.remote.proxyrack import proxyrack_api, utils as pr_utils

logger = logging.getLogger(__name__)


class ProxyRackProxyBackend(backends.ProxyBackend):
    def get_proxy_url(self, ip_fingerprint):
        return self._build_proxy_url(
            proxyIp=ip_fingerprint.ip,
            # session=str(uuid.uuid4()),
        )

    def new_ip_fingerprint(self, fingerprint):
        proxies = utils.proxy_dict(self._test_proxy_url(fingerprint))
        if self.is_valid_proxy(proxies=proxies):
            with Client(proxies=proxies) as client:
                r_stats = proxyrack_api.stats(client)
            ip_fingerprint = IPFingerprint.objects.create(
                city=r_stats.ipinfo.city,
                country=r_stats.ipinfo.country,
                isp=r_stats.ipinfo.isp,
                ip=r_stats.ipinfo.ip,
                fingerprint=fingerprint
            )
            fingerprint.add_ip_fingerprint(ip_fingerprint)
            return ip_fingerprint
        else:
            raise exceptions.DJSpooferError('Failed to get a new valid proxy')

    def is_valid_proxy(self, proxies):
        return proxyrack_api.is_valid_proxy(proxies)

    def _test_proxy_url(self, fingerprint):
        geolocation = fingerprint.geolocation
        return self._build_proxy_url(
            osName=fingerprint.os,
            country=getattr(geolocation, 'country', None),
            city=getattr(geolocation, 'city', None),
            isp=getattr(geolocation, 'isp', None),
        )

    @staticmethod
    def _build_proxy_url(**kwargs):
        return pr_utils.ProxyBuilder(
            username=settings.PROXY_USERNAME,
            password=settings.PROXY_PASSWORD,
            netloc=Proxy.objects.get_rotating_proxy().url,
            timeoutSeconds=60,
            **kwargs
        ).http_url
