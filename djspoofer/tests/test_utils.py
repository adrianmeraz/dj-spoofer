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

    def test_ua_parser(self):
        user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.82 Safari/537.36')
        ua_parser = utils.UserAgentParser(user_agent=user_agent)

        self.assertEquals(
            str(ua_parser),
            ("UserAgentParser -> {'user_agent': {'family': 'Chrome', 'major': '99', 'minor': '0', 'patch': '4844'}, 'os': {'family': 'Windows', 'major': '10', 'minor': None, 'patch': None, 'patch_minor': None}, 'device': {'family': 'Other', 'brand': None, 'model': None}, 'string': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}")
        )

        user_agent = ua_parser._user_agent
        self.assertEquals(user_agent.family, 'Chrome')
        self.assertEquals(user_agent.major, '99')
        self.assertEquals(user_agent.minor, '0')
        self.assertEquals(user_agent.patch, '4844')

        os = ua_parser._os
        self.assertEquals(os.family, 'Windows')
        self.assertEquals(os.major, '10')
        self.assertIsNone(os.minor)
        self.assertIsNone(os.patch)

        self.assertEquals(ua_parser.browser, 'Chrome')
        self.assertEquals(ua_parser.browser_major_version, '99')
        self.assertEquals(ua_parser.os, 'Windows')
