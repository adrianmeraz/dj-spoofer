import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer.remote.proxyrack import proxyrack_api, exceptions


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mocked_sleep = mock.patch('time.sleep', return_value=None).start()


class ProxyRackAPITests(BaseTestCase):
    """
        Proxy Rack API Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.schemas.proxyrack', 'passwords.json') as passwords_json:
            cls.r_data = json.loads(passwords_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.r_data
        )

        r_temp = proxyrack_api.generate_temp_api_key(
            mock_client,
            expiration_seconds=60
        )
        self.assertEquals(r_temp.api_key, 'temp-bf3702-be83a4-0bbfc1-be7f58-62cfff')

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.r_data
        )

        with self.assertRaises(exceptions.ProxyRackError):
            proxyrack_api.generate_temp_api_key(
                mock_client,
                expiration_seconds=60
            )
