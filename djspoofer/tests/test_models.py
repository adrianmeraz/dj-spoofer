from django.test import TestCase

from djspoofer.models import Profile, Proxy


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
            'weight': .005,
        }

    def test_user_str(self):
        profile = Profile.objects.create(**self.profile_data)
        self.assertEqual(str(profile), f'Profile: {profile.user_agent}')


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
        self.assertEqual(str(proxy), f'Proxy: {proxy.url} - {proxy.mode}')

    def test_on_cooldown(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertFalse(proxy.on_cooldown)

        proxy.set_last_used()
        self.assertTrue(proxy.on_cooldown)

    def test_set_last_used(self):
        proxy = Proxy.objects.create(**self.proxy_data)
        self.assertEquals(proxy.used_count, 0)
        self.assertIsNone(proxy.last_used)

        proxy.set_last_used()
        self.assertEquals(proxy.used_count, 1)
        self.assertIsNotNone(proxy.last_used)

    # def test_dupe_username(self):
    #     MarzUser.objects.create(**self.marz_user_data)
    #     with self.assertRaises(IntegrityError):
    #         MarzUser.objects.create(**self.marz_user_data)
    #
    # def test_marz_user_toggle_lock(self):
    #     marz_user = MarzUser.objects.create(**self.marz_user_data)
    #     marz_user.lock()
    #     self.assertTrue(marz_user.is_locked)
    #     marz_user.unlock()
    #     self.assertFalse(marz_user.is_locked)
    #     self.assertIsNone(marz_user.locked_at)
    #
    # def test_marz_user_update_session_info(self):
    #     marz_user = MarzUser.objects.create(**self.marz_user_data)
    #     self.assertEquals(marz_user.session_count, 0)
    #     marz_user.update_session_info()
    #     self.assertEquals(marz_user.session_count, 1)
