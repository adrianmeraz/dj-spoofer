from django.test import TestCase

from djspoofer.models import Fingerprint, Proxy


class ProfileTests(TestCase):
    """
    Profile Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.profile_data = {
            'device_category': 'mobile',
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': 'My User Agent 1.0',
            'viewport_height': 768,
            'viewport_width': 1024,
        }

    def test_user_str(self):
        profile = Fingerprint.objects.create(**self.profile_data)
        self.assertEqual(str(profile), 'Fingerprint -> user_agent: My User Agent 1.0')


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

    def test_on_cooldown(self):
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
