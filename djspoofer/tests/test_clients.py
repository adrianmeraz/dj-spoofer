from unittest import mock

from django.test import TestCase
from httpx import Request

from djspoofer.clients import SpoofedDesktopClient
from djspoofer.models import Fingerprint, Proxy


class SpoofedDesktopClientTests(TestCase):
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
            proxy=proxy
        )

    def test_ok(self):
        with SpoofedDesktopClient(fingerprint=self.fingerprint) as session:
            self.assertEquals(session.proxies['http://'], 'http://user123:password456@example.com:4582')
            self.assertEquals(session.proxies['https://'], 'https://user123:password456@example.com:4582')

            self.assertEquals(session.headers['user-agent'], 'Test User Agent 1.0')
