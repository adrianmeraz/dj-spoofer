from django.test import TestCase

from djspoofer import utils


class UtilTests(TestCase):
    """
    Utility Tests
    """

    def test_fake_profile(self):
        old_profile = utils.FakeProfile()
        profile = utils.FakeProfile()
        self.assertNotEquals(old_profile, profile)

        self.assertIn(profile.gender, ['M', 'F'])
        self.assertIn(profile.full_gender, ['MALE', 'FEMALE'])
        self.assertEquals(profile.full_name, f'{profile.first_name} {profile.last_name}')

        dob = profile.dob
        self.assertEquals(profile.dob_yyyymmdd, f'{dob.year}-{dob.month:02}-{dob.day:02}')
        self.assertTrue(profile.us_phone_number.startswith('+1'))
        self.assertEquals(len(profile.us_phone_number), 12)
