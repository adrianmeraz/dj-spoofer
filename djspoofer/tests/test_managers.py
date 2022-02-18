import datetime

from django.test import TestCase
from django.utils import timezone

from djspoofer import const, exceptions
from djspoofer.models import Profile, Proxy


class ProfileManagerTests(TestCase):
    """
    ProfileManager Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.profile_data = {
            'platform': 'US',
            'screen_height': 1920,
            'screen_width': 1080,
            'user_agent': 'My User Agent 1.0',
            'viewport_height': 768,
            'viewport_width': 1024,
            'weight': .005,
        }

    def test_all_user_agents(self):
        Profile.objects.create(**self.profile_data)

        new_data = self.profile_data.copy()
        new_data['user_agent'] = 'The 2nd User Agent 2.0'
        Profile.objects.create(**new_data)

        user_agents = Profile.objects.all_user_agents()

        self.assertListEqual(
            list(user_agents),
            ['My User Agent 1.0', 'The 2nd User Agent 2.0']
        )

    def test_random_desktop_profile(self):
        with self.assertRaises(exceptions.DJSpooferError):
            Profile.objects.random_desktop_profile()

        Profile.objects.create(device_category='desktop', **self.profile_data)

        profile = Profile.objects.random_desktop_profile()

        self.assertEquals(profile.user_agent, 'My User Agent 1.0')

    def test_weighted_desktop_user_agent(self):
        with self.assertRaises(exceptions.DJSpooferError):
            Profile.objects.weighted_desktop_profile()

        Profile.objects.create(device_category='desktop', **self.profile_data)

        profile = Profile.objects.weighted_desktop_profile()

        self.assertEquals(profile.user_agent, 'My User Agent 1.0')

    def test_weighted_mobile_user_agent(self):
        with self.assertRaises(exceptions.DJSpooferError):
            Profile.objects.weighted_mobile_profile()

        Profile.objects.create(device_category='mobile', **self.profile_data)

        profile = Profile.objects.weighted_mobile_profile()

        self.assertEquals(profile.user_agent, 'My User Agent 1.0')

    def test_older_than_n_minutes(self):
        profile = Profile.objects.create(**self.profile_data)

        self.assertFalse(Profile.objects.older_than_n_minutes().exists())

        profile.created = timezone.now() - datetime.timedelta(minutes=6)
        profile.save()

        self.assertTrue(Profile.objects.older_than_n_minutes().exists())


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
