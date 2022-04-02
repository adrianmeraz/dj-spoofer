from ssl import Options

from django.test import TestCase

from djspoofer.models import Fingerprint, TLSFingerprint, Proxy


class FingerprintTests(TestCase):
    """
    Fingerprint Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.fingerprint_data = {
            'device_category': 'mobile',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/99.0.4844.74 Safari/537.36'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }

    def test_user_str(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        self.assertEqual(str(fp), f'Fingerprint -> user_agent: {self.fingerprint_data["user_agent"]}')

    def test_is_desktop(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        self.assertFalse(fp.is_desktop)

    def test_is_mobile(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        self.assertTrue(fp.is_mobile)

    def test_ua_browser(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        self.assertTrue(fp.ua_browser)

    def test_ua_platform(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        self.assertTrue(fp.ua_platform)


class TLSFingerprintTests(TestCase):
    """
    TLSFingerprint Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.fingerprint_data = {
            'device_category': 'mobile',
            'platform': 'Chrome',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/99.0.4844.74 Safari/537.36'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }

    def test_ciphers(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        tls_fp = TLSFingerprint.objects.create(fingerprint=fp)
        self.assertTrue(':' in tls_fp.ciphers)

    def test_extensions(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        tls_fp = TLSFingerprint.objects.create(fingerprint=fp)
        self.assertEquals(type(tls_fp.extensions), int)

        tls_fp.extensions = int(Options.OP_NO_TICKET | Options.OP_NO_RENEGOTIATION | Options.OP_ENABLE_MIDDLEBOX_COMPAT)
        self.assertEquals(tls_fp.extensions, 1074806784)


class ProxyTests(TestCase):
    """
    Proxy Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.proxy_data = {
            'url': 'user123:password456@example.com:4582',
            'country': 'US',
            'city': 'dallas',
        }

    def test_user_str(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertEqual(str(proxy), 'Proxy -> url: user123:password456@example.com:4582, mode: GENERAL')

    def test_is_on_cooldown(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertFalse(proxy.is_on_cooldown)

        proxy.set_last_used()
        self.assertTrue(proxy.is_on_cooldown)

    def test_set_last_used(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertEquals(proxy.used_count, 0)
        self.assertIsNone(proxy.last_used)

        proxy.set_last_used()
        self.assertEquals(proxy.used_count, 1)
        self.assertIsNotNone(proxy.last_used)

    def test_http_url(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertEquals(proxy.http_url, 'http://user123:password456@example.com:4582')

    def test_https_url(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertEquals(proxy.https_url, 'https://user123:password456@example.com:4582')

