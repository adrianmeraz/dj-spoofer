from unittest import mock

from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer import clients
from djspoofer.models import Fingerprint, Proxy


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
        cls.fingerprint = Fingerprint.objects.create(
            device_category='desktop',
            platform='windows',
            screen_height=1080,
            screen_width=1920,
            user_agent='Test User Agent 1.0',
            viewport_height=1080,
            viewport_width=1920,
            # proxy=proxy
        )

    @mock.patch.object(clients.DesktopChromeClient, '_send_handling_auth')
    def test_ok(self, mock_sd_send):
        mock_sd_send.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            text='ok'
        )
        with clients.DesktopChromeClient(fingerprint=self.fingerprint) as sd_client:
            sd_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)


class DesktopFirefoxClientTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        cls.mocked_sleep = mock.patch('time.sleep', return_value=None).start()
        proxy = Proxy.objects.create_general_proxy(
            url='user123:password456@example.com:4582'
        )
        cls.proxy = proxy
        cls.fingerprint = Fingerprint.objects.create(
            device_category='desktop',
            platform='windows',
            screen_height=1080,
            screen_width=1920,
            user_agent='Test User Agent 1.0',
            viewport_height=1080,
            viewport_width=1920,
            # proxy=proxy
        )

    @mock.patch.object(clients.DesktopFirefoxClient, '_send_handling_auth')
    def test_ok(self, mock_sd_send):
        mock_sd_send.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            text='ok'
        )
        with clients.DesktopFirefoxClient(fingerprint=self.fingerprint) as sd_client:
            sd_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)
