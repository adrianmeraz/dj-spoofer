from django.test import TestCase

from djspoofer.remote.intoli import exceptions
from djspoofer.models import Profile


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

    def test_all_oids(self):
        profile = Profile.objects.create(device_category='desktop', **self.profile_data)

        self.assertEquals(list(Profile.objects.all_oids()), [profile.oid])

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

    def test_random_desktop_chrome_profile(self):
        with self.assertRaises(exceptions.IntoliError):
            Profile.objects.random_desktop_profile()

        Profile.objects.create(browser='Chrome', device_category='desktop', os='Windows', **self.profile_data)

        profile = Profile.objects.random_desktop_profile()

        self.assertEquals(profile.user_agent, 'My User Agent 1.0')

    def test_random_mobile_profile(self):
        with self.assertRaises(exceptions.IntoliError):
            Profile.objects.random_mobile_profile()

        Profile.objects.create(device_category='mobile', **self.profile_data)

        profile = Profile.objects.random_mobile_profile()

        self.assertEquals(profile.user_agent, 'My User Agent 1.0')

    def test_weighted_desktop_chrome_user_agent(self):
        with self.assertRaises(exceptions.IntoliError):
            Profile.objects.weighted_desktop_profile()

        Profile.objects.create(browser='Chrome', device_category='desktop', os='Windows', **self.profile_data)

        profile = Profile.objects.weighted_desktop_profile()

        self.assertEquals(profile.user_agent, 'My User Agent 1.0')

    def test_weighted_mobile_user_agent(self):
        with self.assertRaises(exceptions.IntoliError):
            Profile.objects.weighted_mobile_profile()

        Profile.objects.create(device_category='mobile', **self.profile_data)

        profile = Profile.objects.weighted_mobile_profile()

        self.assertEquals(profile.user_agent, 'My User Agent 1.0')

    def test_bulk_delete(self):
        profile = Profile.objects.create(device_category='desktop', os='Linux', **self.profile_data)

        Profile.objects.bulk_delete(oids=[profile.oid])

        with self.assertRaises(Profile.DoesNotExist):
            profile.refresh_from_db()
