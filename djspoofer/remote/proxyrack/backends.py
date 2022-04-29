import logging
import uuid

from django.conf import settings
from httpx import Client

from djspoofer import backends, exceptions, utils
from djspoofer.models import IPFingerprint, Proxy
from djspoofer.remote.proxyrack import proxyrack_api, utils as pr_utils

logger = logging.getLogger(__name__)


class ProxyRackProxyBackend(backends.ProxyBackend):
    def get_proxy_url(self, fingerprint):
        for ip_fingerprint in fingerprint.get_last_n_ip_fingerprints(count=3):
            proxy_url = self._build_proxy_url(proxyIp=ip_fingerprint.ip)
            if self._is_valid_proxy(proxies=utils.proxy_dict(proxy_url)):
                logger.info(f'Found valid IP Fingerprint: {ip_fingerprint}')
                return proxy_url
        else:
            logger.info(f'No valid IP Fingerprints found. {fingerprint}')
            return self._new_proxy_url(fingerprint)   # Generate if no valid IP Fingerprints

    def _new_proxy_url(self, fingerprint):
        proxy_url = self._test_proxy_url(fingerprint)
        proxies = utils.proxy_dict(proxy_url)
        if self._is_valid_proxy(proxies=proxies):
            self._create_ip_fingerprint(fingerprint, proxies)
            return proxy_url
        raise exceptions.DJSpooferError('Failed to get a new valid proxy')

    @staticmethod
    def _is_valid_proxy(proxies):
        return proxyrack_api.is_valid_proxy(proxies)

    @staticmethod
    def _create_ip_fingerprint(fingerprint, proxies):
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
        logger.info(f'Successfully created new ip fingerprint: {ip_fingerprint}')

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
            session=str(uuid.uuid4()),
            **kwargs
        ).http_url
