from django.test import TestCase

from djspoofer import const
from djspoofer.models import Proxy


class ProxyManagerTests(TestCase):
    """
    ProxyManager Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.proxy_data = {
            'url': 'user123:password456@example.com:4582',
            'country': 'US',
            'city': 'dallas',
        }
        cls.proxy_data_2 = {
            'url': 'another123:password456@example.com:4582',
            'country': 'US',
            'city': 'dallas',
        }

    def test_get_rotating_proxy(self):
        Proxy.objects.create(**self.proxy_data)
        with self.assertRaises(Proxy.DoesNotExist):
            Proxy.objects.get_rotating_proxy()

        Proxy.objects.create(mode=const.ProxyModes.ROTATING.value, **self.proxy_data_2)
        self.assertIsNotNone(Proxy.objects.get_rotating_proxy())

    def test_get_sticky_proxy(self):
        Proxy.objects.create(**self.proxy_data)
        with self.assertRaises(Proxy.DoesNotExist):
            Proxy.objects.get_sticky_proxy()

        Proxy.objects.create(mode=const.ProxyModes.STICKY.value, **self.proxy_data_2)
        self.assertIsNotNone(Proxy.objects.get_sticky_proxy())

    def test_get_all_urls(self):
        Proxy.objects.create(**self.proxy_data)
        Proxy.objects.create(mode=const.ProxyModes.STICKY.value, **self.proxy_data_2)

        self.assertListEqual(
            sorted(list(Proxy.objects.get_all_urls())),
            sorted([self.proxy_data['url'], self.proxy_data_2['url']])
        )
