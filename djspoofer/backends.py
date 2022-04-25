import logging
from abc import ABC

logger = logging.getLogger(__name__)


class ProxyBackend(ABC):

    def proxy_url(self, ip_fingerprint):
        raise NotImplemented

    def is_valid_proxy(self, proxies):
        raise NotImplemented

    def new_ip_fingerprint(self, fingerprint):
        raise NotImplemented

    @staticmethod
    def proxy_dict(proxy_url):
        if proxy_url:
            return {
                'http://': proxy_url,
                'https://': proxy_url,
            }
        return dict()
