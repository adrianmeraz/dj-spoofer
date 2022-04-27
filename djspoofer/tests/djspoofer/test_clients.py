import json
from importlib.resources import open_text
from unittest import mock

from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer import clients, utils
from djspoofer.models import Fingerprint, IPFingerprint, Proxy, Geolocation
from djspoofer.remote.proxyrack import proxyrack_api


class DesktopChromeClientTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.proxy = Proxy.objects.create_rotating_proxy(
            url='test123:5000',
        )
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
        cls.ip_fingerprint_data = {
            'city': 'Los Angeles',
            'country': 'US',
            'isp': 'Spectrum',
            'ip': '194.60.86.250',
        }
        cls.geo_location_data = {
            'city': 'Los Angeles',
            'country': 'US',
            'isp': 'Spectrum',
        }
        with open_text('djspoofer.tests.proxyrack.resources', 'stats.json') as stats_json:
            cls.r_stats_data = proxyrack_api.StatsResponse(json.loads(stats_json.read()))

    @mock.patch.object(proxyrack_api, 'stats')
    @mock.patch.object(proxyrack_api, 'is_valid_proxy')
    @mock.patch.object(clients.DesktopChromeClient, '_send_handling_auth')
    def test_ok(self, mock_sd_send, mock_is_valid_proxy, mock_stats):
        mock_sd_send.return_value = Response(
            request=Request(url='', method=''),
            status_code=codes.OK,
            text='ok'
        )
        mock_is_valid_proxy.return_value = True
        mock_stats.return_value = self.r_stats_data

        with clients.DesktopChromeClient(fingerprint=self.fingerprint) as chrome_client:
            chrome_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)
            self.assertEquals(
                chrome_client.sec_ch_ua,
                '" Not;A Brand";v="99", "Google Chrome";v="99", "Chromium";v="99"'
            )
            self.assertEquals(chrome_client.sec_ch_ua_mobile, '?0')
            self.assertEquals(chrome_client.sec_ch_ua_platform, '"Windows"')

    @mock.patch.object(proxyrack_api, 'stats')
    @mock.patch.object(proxyrack_api, 'is_valid_proxy')
    @mock.patch.object(clients.DesktopChromeClient, '_send_handling_auth')
    def test_fingerprint_with_geolocation_no_ips(self, mock_sd_send, mock_is_valid_proxy, mock_stats):
        mock_sd_send.return_value = Response(
            request=Request(url='', method=''),
            status_code=codes.OK,
            text='ok'
        )
        mock_is_valid_proxy.return_value = True
        mock_stats.return_value = self.r_stats_data

        self.fingerprint.set_geolocation(Geolocation.objects.create(**self.geo_location_data))

        with clients.DesktopChromeClient(fingerprint=self.fingerprint) as chrome_client:
            chrome_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)
            self.assertEquals(
                chrome_client.sec_ch_ua,
                '" Not;A Brand";v="99", "Google Chrome";v="99", "Chromium";v="99"'
            )
            self.assertEquals(chrome_client.sec_ch_ua_mobile, '?0')
            self.assertEquals(chrome_client.sec_ch_ua_platform, '"Windows"')


class DesktopFirefoxClientTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.proxy = Proxy.objects.create_rotating_proxy(
            url='test123:5000',
        )
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'
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
    @mock.patch.object(clients.DesktopFirefoxClient, '_send_handling_auth')
    def test_ok(self, mock_sd_send, mock_is_valid_proxy, mock_stats):
        mock_sd_send.return_value = Response(
            request=Request(url='', method=''),
            status_code=codes.OK,
            text='ok'
        )
        mock_is_valid_proxy.return_value = True
        mock_stats.return_value = self.r_stats_data

        with clients.DesktopFirefoxClient(fingerprint=self.fingerprint) as sd_client:
            sd_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)


