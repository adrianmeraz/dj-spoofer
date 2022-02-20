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

    def test_ok(self):

        proxy_url = 'user123:password456@example.com:4582'
        user_agent = 'My User Agent 1.0'

        Proxy.objects.create('')

        with SpoofedDesktopClient(proxy_url=proxy_url, user_agent=user_agent) as session:
            self.assertEquals(session.proxies['http://'], 'http://user123:password456@example.com:4582')
            self.assertEquals(session.proxies['https://'], 'https://user123:password456@example.com:4582')

            self.assertEquals(session.headers['User-Agent'], user_agent)
