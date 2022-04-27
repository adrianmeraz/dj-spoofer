import json
from importlib.resources import open_text
from unittest import mock

from django.test import TestCase

from djspoofer import utils
from djspoofer.models import Fingerprint, Proxy, IPFingerprint
from djspoofer.remote.proxyrack import proxyrack_api, backends


class ProxyRackProxyBackendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        ua_parser = utils.UserAgentParser(user_agent)
        cls.fingerprint = Fingerprint.objects.create(
            browser=ua_parser.browser,
            device_category='desktop',
            os=ua_parser.os,
            platform='US',
            screen_height=1920,
            screen_width=1080,
            user_agent=user_agent,
            viewport_height=768,
            viewport_width=1024,
        )
        with open_text('djspoofer.tests.proxyrack.resources', 'stats.json') as stats_json:
            cls.r_stats_data = proxyrack_api.StatsResponse(json.loads(stats_json.read()))

    @mock.patch.object(proxyrack_api, 'stats')
    @mock.patch.object(proxyrack_api, 'is_valid_proxy')
    def test_no_geolocation(self, mock_is_valid_proxy, mock_stats):
        mock_is_valid_proxy.return_value = True
        mock_stats.return_value = self.r_stats_data

        Proxy.objects.create_rotating_proxy(url='test123:5000')

        ip_fingerprint = backends.ProxyRackProxyBackend().new_ip_fingerprint(self.fingerprint)
        # Now a geolocation exists
        self.assertIsInstance(ip_fingerprint, IPFingerprint)

