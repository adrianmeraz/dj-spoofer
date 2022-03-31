from unittest import mock

from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer import clients
from djspoofer.models import Fingerprint, Proxy, TLSFingerprint


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
        fingerprint = Fingerprint.objects.create(
            device_category='desktop',
            platform='linux',
            screen_height=1080,
            screen_width=1920,
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            viewport_height=1080,
            viewport_width=1920,
            # proxy=proxy
        )
        cls.fingerprint = fingerprint
        cls.tls_fingerprint = TLSFingerprint.objects.create(
            extensions=123456789,
            ciphers='ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM',
            fingerprint=fingerprint,
        )

    @mock.patch.object(clients.DesktopChromeClient, '_send_handling_auth')
    def test_ok(self, mock_sd_send):
        mock_sd_send.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            text='ok'
        )
        with clients.DesktopChromeClient(fingerprint=self.fingerprint) as chrome_client:
            chrome_client.get('http://example.com')
            self.assertEquals(mock_sd_send.call_count, 1)
            self.assertEquals(
                chrome_client.sec_ch_ua,
                '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"'
            )
            self.assertEquals(chrome_client.sec_ch_ua_mobile, '?0')
            self.assertEquals(chrome_client.sec_ch_ua_platform, '"Linux"')


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
        fingerprint = Fingerprint.objects.create(
            device_category='desktop',
            platform='windows',
            screen_height=1080,
            screen_width=1920,
            user_agent='Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            viewport_height=1080,
            viewport_width=1920,
            # proxy=proxy
        )
        cls.fingerprint = fingerprint
        cls.tls_fingerprint = TLSFingerprint.objects.create(
            extensions=123456789,
            ciphers='ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM',
            fingerprint=fingerprint,
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
