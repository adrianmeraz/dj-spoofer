from django.test import TestCase

from djspoofer import const, exceptions
from djspoofer.models import Fingerprint, Proxy


class FingerprintManagerTests(TestCase):
    """
    FingerprintManager Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.fingerprint_data = {
            'browser': 'Chrome',
            'device_category': 'desktop',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/99.0.4844.74 Safari/537.36'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }

    def test_get_random_desktop_fingerprint(self):
        with self.assertRaises(exceptions.DJSpooferError):
            Fingerprint.objects.get_random_desktop_fingerprint()

        Fingerprint.objects.create(**self.fingerprint_data)
        self.assertIsNotNone(Fingerprint.objects.get_random_desktop_fingerprint())


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
        with self.assertRaises(exceptions.DJSpooferError):
            Proxy.objects.get_rotating_proxy()

        Proxy.objects.create(mode=const.ProxyModes.ROTATING.value, **self.proxy_data_2)
        self.assertIsNotNone(Proxy.objects.get_rotating_proxy())

    def test_get_sticky_proxy(self):
        Proxy.objects.create(**self.proxy_data)
        with self.assertRaises(exceptions.DJSpooferError):
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