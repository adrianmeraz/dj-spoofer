from django.test import TestCase

from intoli.models import Profile


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
        self.assertEqual(str(profile), 'Profile -> user_agent: My User Agent 1.0')
