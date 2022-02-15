from unittest import mock
from importlib.resources import open_binary

import httpx
import json
from django.test import TestCase
from httpx import Request, Response, codes

from intoli import intoli_api, clients


class GetBroadcastsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception

    @mock.patch.object(clients, 'IntoliClient')
    def test_ok(self, mock_client):
        with open_binary('intoli.tests.schemas.intoli', 'user-agents.json.gz') as intoli_gz:
            mock_client.stream.return_value = Response(
                request=self.request,
                status_code=codes.OK,
                content=intoli_gz
            )

        r_profiles = intoli_api.get_profiles(
            mock_client,
        )
