import json
from importlib.resources import open_text
from unittest import mock

import httpx
from django.test import TestCase
from httpx import Request, Response, codes

from djspoofer.remote.twocaptcha import twocaptcha_api, exceptions


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mocked_sleep = mock.patch('time.sleep', return_value=None).start()


class GetSolvedCaptchaTests(BaseTestCase):
    """
        Get Captcha ID Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.twocaptcha.resources', 'get_captcha_id.json') as get_captcha_id_json:
            cls.r_data = json.loads(get_captcha_id_json.read())
        cls.gcaptcha_token = (
            '03AHJ_Vuve5Asa4koK3KSMyUkCq0vUFCR5Im4CwB7PzO3dCxIo11i53epEraq-uBO5mVm2XRikL8iKOWr0aG50sCuej9bXx5'
            'qcviUGSm4iK4NC_Q88flavWhaTXSh0VxoihBwBjXxwXuJZ-WGN5Sy4dtUl2wbpMqAj8Zwup1vyCaQJWFvRjYGWJ_TQBKTXNB'
            '5CCOgncqLetmJ6B6Cos7qoQyaB8ZzBOTGf5KSP6e-K9niYs772f53Oof6aJeSUDNjiKG9gN3FTrdwKwdnAwEYX-F37sI_vLB'
            '1Zs8NQo0PObHYy0b0sf7WSLkzzcIgW9GR0FwcCCm1P8lB-50GQHPEBJUHNnhJyDzwRoRAkVzrf7UkV8wKCdTwrrWqiYDgbrz'
            'URfHc2ESsp020MicJTasSiXmNRgryt-gf50q5BMkiRH7osm4DoUgsjc_XyQiEmQmxl5sqZP7aKsaE-EM00x59XsPzD3m3YI6'
            'SRCFRUevSyumBd7KmXE8VuzIO9lgnnbka4-eZynZa6vbB9cO3QjLH0xSG3-egcplD1uLGh79wC34RF49Ui3eHwua4S9XHpH6'
            'YBe7gXzz6_mv-o-fxrOuphwfrtwvvi2FGfpTexWvxhqWICMFTTjFBCEGEgj7_IFWEKirXW2RTZCVF0Gid7EtIsoEeZkPbrcU'
            'ISGmgtiJkJ_KojuKwImF0G0CsTlxYTOU2sPsd5o1JDt65wGniQR2IZufnPbbK76Yh_KI2DY4cUxMfcb2fAXcFMc9dcpHg6f9'
            'wBXhUtFYTu6pi5LhhGuhpkiGcv6vWYNxMrpWJW_pV7q8mPilwkAP-zw5MJxkgijl2wDMpM-UUQ_k37FVtf-ndbQAIPG7S469'
            'doZMmb5IZYgvcB4ojqCW3Vz6Q'
        )

    @mock.patch.object(twocaptcha_api, 'get_solved_token')
    @mock.patch.object(twocaptcha_api, 'get_captcha_id')
    def test_ok(self, mock_get_captcha_id, mock_get_solved_token):
        mock_get_captcha_id.return_value = '2122988149'
        mock_get_solved_token.return_value = twocaptcha_api.SolvedTokenResponse(
            g_token=self.gcaptcha_token,
            captcha_id='2122988149'
        )

        with httpx.Client() as client:
            r_captcha = twocaptcha_api.get_solved_captcha(
                client,
                proxy='http://example.com:1000',
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com'
            )
            self.assertEquals(r_captcha.g_token, self.gcaptcha_token)
            self.assertEquals(r_captcha.captcha_id, '2122988149')


class GetCaptchaIDTests(BaseTestCase):
    """
        Get Captcha ID Tests
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.twocaptcha.resources', 'get_captcha_id.json') as get_captcha_id_json:
            cls.r_data = json.loads(get_captcha_id_json.read())

    @mock.patch.object(httpx, 'Client')
    def test_ok(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json={
                "status": 1,
                "request": "2122988149"
            }
        )

        captcha_id = twocaptcha_api.get_captcha_id(
            mock_client,
            proxy='http://example.com:1000',
            site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
            page_url='https://example.com'
        )
        self.assertEquals(captcha_id, '2122988149')

    @mock.patch.object(httpx, 'Client')
    def test_invalid_response(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json={
                "status": 0,
                "request": "2122988149"
            }
        )

        with self.assertRaises(exceptions.InvalidResponse):
            twocaptcha_api.get_captcha_id(
                mock_client,
                proxy='http://example.com:1000',
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com'
            )

    @mock.patch.object(httpx, 'Client')
    def test_warn_error(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json={
                "status": 1,
                "request": "ERROR_WRONG_CAPTCHA_ID"
            }
        )

        with self.assertRaises(exceptions.TwoCaptchaError):
            twocaptcha_api.get_captcha_id(
                mock_client,
                proxy='http://example.com:1000',
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com'
            )

    @mock.patch.object(httpx, 'Client')
    def test_critical_error(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json={
                "status": 1,
                "request": "ERROR_WRONG_USER_KEY"
            }
        )

        with self.assertRaises(exceptions.CriticalError):
            twocaptcha_api.get_captcha_id(
                mock_client,
                proxy='http://example.com:1000',
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com'
            )

    @mock.patch.object(httpx, 'Client')
    def test_captcha_unsolveable(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json={
                "status": 1,
                "request": "ERROR_CAPTCHA_UNSOLVABLE"
            }
        )

        with self.assertRaises(exceptions.CaptchaUnsolvable):
            twocaptcha_api.get_captcha_id(
                mock_client,
                proxy='http://example.com:1000',
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com'
            )

    @mock.patch.object(httpx, 'Client')
    def test_captcha_not_ready(self, mock_client):
        mock_client.post.return_value = Response(
            request=self.request,
            status_code=codes.OK,
            json={
                "status": 1,
                "request": "CAPCHA_NOT_READY"
            }
        )

        with self.assertRaises(exceptions.CaptchaNotReady):
            twocaptcha_api.get_captcha_id(
                mock_client,
                proxy='http://example.com:1000',
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com'
            )