from ssl import Options

from django.test import TestCase

from djspoofer.models import Geolocation, Fingerprint, IPFingerprint, Proxy, TLSFingerprint
from djspoofer import utils


class FingerprintTests(TestCase):
    """
    Fingerprint Tests
    """

    @classmethod
    def setUpTestData(cls):
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'
        ua_parser = utils.UserAgentParser(user_agent)
        cls.fingerprint_data = {
            'browser': ua_parser.browser,
            'device_category': 'mobile',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/99.0.4844.74 Safari/537.36'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }
        cls.ip_fingerprint_data = {
            'city': 'Los Angeles',
            'country': 'US',
            'isp': 'Spectrum',
            'ip': '194.60.86.250',
        }

    def test_str(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        self.assertEqual(str(fp), f'Fingerprint -> user_agent: {self.fingerprint_data["user_agent"]}')

    def test_ok(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        self.assertEquals(fp.tls_fingerprint.browser, fp.browser)

    def test_set_geolocation(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        geolocation = Geolocation.objects.create(city='Los Angeles')
        fp.set_geolocation(geolocation)
        self.assertEquals(fp.tls_fingerprint.browser, fp.browser)

    def test_get_first_n_ip_fingerprints(self):
        fp = Fingerprint.objects.create(**self.fingerprint_data)
        self.assertEquals(fp.get_last_n_ip_fingerprints(3).count(), 0)

        for _ in range(6):
            fp.add_ip_fingerprint(IPFingerprint.objects.create(**self.ip_fingerprint_data))

        self.assertEquals(fp.get_last_n_ip_fingerprints(4).count(), 4)

    def test_add_ip_fingerprint(self):
        fingerprint = Fingerprint.objects.create(**self.fingerprint_data)

        self.assertIsNone(fingerprint.geolocation)

        ip_fingerprint = IPFingerprint.objects.create(**self.ip_fingerprint_data)
        fingerprint.add_ip_fingerprint(ip_fingerprint)

        self.assertEquals(fingerprint.ip_fingerprints.all().count(), 1)
        self.assertEquals(fingerprint.geolocation.isp, 'Spectrum')


class IPFingerprintTests(TestCase):
    """
    IPFingerprint Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.ip_fingerprint_data = {
            'city': 'Dallas',
            'country': 'US',
            'isp': 'Spectrum',
            'ip': '194.60.86.250',
        }
        cls.fingerprint_data = {
            'browser': 'Chrome',
            'device_category': 'mobile',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/99.0.4844.74 Safari/537.36'),
            'viewport_height': 768,
            'viewport_width': 1024,
        }

    def test_str(self):
        ip_fingerprint = IPFingerprint.objects.create(
            **self.ip_fingerprint_data,
        )
        self.assertEqual(str(ip_fingerprint), f'IPFingerprint -> ip: 194.60.86.250')


class TLSFingerprintTests(TestCase):
    """
    TLSFingerprint Tests
    """

    @classmethod
    def setUpTestData(cls):
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'
        ua_parser = utils.UserAgentParser(user_agent)
        cls.tls_fingerprint_data = {
            'browser': ua_parser.browser,
        }

    def test_ciphers(self):
        tls_fp = TLSFingerprint.objects.create(**self.tls_fingerprint_data)
        self.assertTrue(':' in tls_fp.ciphers)

    def test_extensions(self):
        tls_fp = TLSFingerprint.objects.create(**self.tls_fingerprint_data)
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

    def test_str(self):
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
        self.assertTrue(proxy.http_url, 'http://user123:password456@example.com:4582')

    def test_https_url(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertEquals(proxy.https_url, 'https://user123:password456@example.com:4582')

