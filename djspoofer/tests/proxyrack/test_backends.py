import json
from importlib.resources import open_text

from django.test import TestCase

from djspoofer import utils
from djspoofer.models import Fingerprint
from djspoofer.remote.proxyrack import proxyrack_api


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
