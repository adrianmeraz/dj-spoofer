import json
from importlib.resources import open_text
from unittest import mock

from django.test import TestCase
from httpx import Request

from djspoofer.models import Profile
from djspoofer.remote.intoli import tasks, intoli_api


class GetProfilesTaskTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.request = Request(url='', method='')  # Must add a non null request to avoid raising Runtime exception
        with open_text('djspoofer.tests.intoli.resources', 'user-agents.json') as user_agents_json:
            cls.r_data = json.loads(user_agents_json.read())

    @mock.patch.object(intoli_api, 'get_profiles')
    def test_ok(self, get_profiles):
        get_profiles.return_value = intoli_api.GetProfilesResponse(self.r_data)

        tasks.get_profiles()
        self.assertEquals(Profile.objects.count(), 5)
