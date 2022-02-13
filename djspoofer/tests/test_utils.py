from django.test import TestCase

from djspoofer import utils


class UtilTests(TestCase):
    """
    Utility Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.test_str = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'

    def test_spoof_session(self):
        test_proxy = 'user123:password456@example.com:4582'
        user_agent = 'My User Agent 1.0'
        with utils.SpoofSession(proxy_str=test_proxy, user_agent=user_agent) as session:
            self.assertEquals(session.proxies['http://'], f'http://{test_proxy}/')
            self.assertEquals(session.proxies['https://'], f'https://{test_proxy}/')

            self.assertEquals(session.headers['User-Agent'], user_agent)

            new_headers = {
                'accept': 'application/json',
                'accept-encoding': 'gzip, deflate, br',
                'empty-header': '',
                'accept-language': 'en-US,en;q=0.9',
            }
            session.update_headers(new_headers)

            self.assertDictEqual(
                dict(session.headers),
                {
                    'accept': 'application/json',
                    'accept-encoding': 'gzip, deflate, br',
                    'connection': 'keep-alive',
                    'user-agent': 'My User Agent 1.0',
                    'accept-language': 'en-US,en;q=0.9'
                }
            )

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
