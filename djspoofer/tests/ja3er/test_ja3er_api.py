import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from djspoofer.remote.ja3er import exceptions, ja3er_api
from httpx import Request, Response, codes


class DetailsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.ja3er.schemas', 'details.json') as details_json:
            cls.details_json = json.loads(details_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json=self.details_json
        )

        r_details = ja3er_api.details(
            mock_client,
        )
        self.assertEquals(r_details.ssl_version, '771')
        self.assertEquals(
            r_details.ciphers,
            '4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53'
        )
        self.assertEquals(r_details.ssl_extensions, '0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21')
        self.assertEquals(r_details.elliptic_curve, '29-23-24')
        self.assertEquals(r_details.elliptic_curve_point_format, '0')

    @mock.patch.object(httpx, 'Client')
    def test_400(self, mock_client):
        mock_client.get.return_value = Response(
            request=self.request,
            status_code=codes.BAD_REQUEST,
            json=self.details_json
        )

        with self.assertRaises(exceptions.Ja3erError):
            ja3er_api.details(
                mock_client,
            )
