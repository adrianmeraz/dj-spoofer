from unittest import mock

from django.test import TestCase
from httpx import Request

from djspoofer.clients import SpoofedDesktopSession


class FXClientTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        cls.mocked_sleep = mock.patch('time.sleep', return_value=None).start()

    def test_ok(self):
        proxy_url = 'https://user123:password456@example.com:4582'
        user_agent = 'My User Agent 1.0'
        with SpoofedDesktopSession(proxy_url=proxy_url, user_agent=user_agent) as session:
            self.assertEquals(session.proxies['http://'], f'http://{proxy_url}/')
            self.assertEquals(session.proxies['https://'], f'https://{proxy_url}/')

            self.assertEquals(session.headers['User-Agent'], user_agent)
