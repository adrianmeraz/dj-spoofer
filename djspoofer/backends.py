import logging
from abc import ABC

logger = logging.getLogger(__name__)


class ProxyBackend(ABC):

    def get_proxy_url(self, ip_fingerprint):
        raise NotImplemented

    def is_valid_proxy(self, proxies):
        raise NotImplemented

    def new_ip_fingerprint(self, fingerprint):
        raise NotImplemented
