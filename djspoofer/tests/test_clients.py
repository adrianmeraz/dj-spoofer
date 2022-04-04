from unittest import mock

from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer import clients
from djspoofer.models import Proxy
from intoli.models import Profile


class DesktopChromeClientTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        cls.mocked_sleep = mock.patch('time.sleep', return_value=None).start()
        proxy = Proxy.objects.create_general_proxy(
            url='user123:password456@example.com:4582'
        )
        cls.proxy = proxy
        Profile.objects.create(
            browser='Chrome',
            device_category='desktop',
            os='Windows',
            platform='US',
            screen_height=1920,
            screen_width=1080,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            viewport_height=768,
            viewport_width=1024,
            weight=.005,
        )

    @mock.patch.object(clients.DesktopChromeClient, '_send_handling_auth')
    def test_ok(self, mock_sd_send):
        mock_sd_send.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            text='ok'
        )
        with clients.DesktopChromeClient() as chrome_client:
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
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        cls.mocked_sleep = mock.patch('time.sleep', return_value=None).start()
        Profile.objects.create(
            browser='Firefox',
            device_category='desktop',
            os='Linux',
            platform='US',
            screen_height=1920,
            screen_width=1080,
            user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0',
            viewport_height=768,
            viewport_width=1024,
            weight=.005,
        )
        proxy = Proxy.objects.create_general_proxy(
            url='user123:password456@example.com:4582'
        )
        cls.proxy = proxy

    @mock.patch.object(clients.DesktopFirefoxClient, '_send_handling_auth')
    def test_ok(self, mock_sd_send):
        mock_sd_send.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            text='ok'
        )
        with clients.DesktopFirefoxClient() as sd_client:
            sd_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)


