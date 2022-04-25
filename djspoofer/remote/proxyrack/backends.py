import uuid

from django.conf import settings
from djstarter.clients import Http2Client

from djspoofer import backends, exceptions
from djspoofer.models import IPFingerprint, Proxy
from djspoofer.remote.proxyrack import proxyrack_api, utils as pr_utils


class ProxyRackProxyBackend(backends.ProxyBackend):
    def proxy_url(self, ip_fingerprint):
        return self._build_proxy_url(
            country=ip_fingerprint.country,
            city=ip_fingerprint.city,
            isp=ip_fingerprint.isp,
            proxyIp=ip_fingerprint.ip,
            osName=ip_fingerprint.fingerprint.os
        )

    def is_valid_proxy(self, proxies):
        return proxyrack_api.is_valid_proxy(proxies)

    def new_ip_fingerprint(self, fingerprint):
        test_proxy_url = self._test_proxy_url(fingerprint)
        if self.is_valid_proxy(proxies=self.proxy_dict(test_proxy_url)):
            with Http2Client(proxies=self._proxy_dict(test_proxy_url)) as client:
                r_stats = proxyrack_api.stats(client)
                return IPFingerprint.objects.create(
                    city=r_stats.ipinfo.city,
                    country=r_stats.ipinfo.country,
                    isp=r_stats.ipinfo.isp,
                    ip=r_stats.ipinfo.ip,
                    fingerprint=fingerprint
                )
        else:
            raise exceptions.DJSpooferError('Failed to get a valid proxy')

    @staticmethod
    def _proxy_dict(proxy_url):
        return {
            'http://': proxy_url,
            'https://': proxy_url
        }

    def _test_proxy_url(self, fingerprint):
        if fingerprint.geolocation:
            return self._new_geolocated_proxy_url(fingerprint)
        else:
            return self._new_generic_proxy_url(fingerprint)

    def _new_geolocated_proxy_url(self, fingerprint):
        return self._build_proxy_url(
            country=fingerprint.geolocation.country,
            city=fingerprint.geolocation.city,
            isp=fingerprint.geolocation.isp,
            osName=fingerprint.os
        )

    def _new_generic_proxy_url(self, fingerprint):
        return self._build_proxy_url(
            country=pr_utils.proxy_weighted_country(),
            # isp=pr_utils.proxy_weighted_isp(),  # TODO Map ISPs with countries or maybe omit
            osName=fingerprint.os
        )

    @staticmethod
    def _build_proxy_url(**kwargs):
        proxy = Proxy.objects.get_rotating_proxy()
        proxy_builder = pr_utils.ProxyBuilder(
            username=settings.PROXY_USERNAME,
            password=settings.PROXY_PASSWORD,
            netloc=proxy.url,
            refreshMinutes=10,
            session=str(uuid.uuid4()),
            **kwargs
        )
        return proxy_builder.http_url
