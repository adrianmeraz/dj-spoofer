import logging
import random
from collections import OrderedDict

from faker import Faker
from httpx import Client

from . import models, providers

logger = logging.getLogger(__name__)


class SpoofSession(Client):
    def __init__(self, proxy_str=None, user_agent=None):
        self.proxies = {
            'http://': f'http://{proxy_str}/',
            'https://': f'https://{proxy_str}/'
        }
        self.headers = {
            'User-Agent': user_agent or models.Profile.objects.weighted_desktop_user_agent()
        }
        super().__init__(proxies=self.proxies, headers=self.headers)

    def update_headers(self, new_headers):
        self.headers = OrderedDict({**self.headers, **self.clean_headers(new_headers)})

    @classmethod
    def clean_headers(cls, headers):
        return OrderedDict({k: v for k, v in headers.items() if v})


fake = Faker('en_US')
fake.add_provider(providers.UsernameProvider)
fake.add_provider(providers.PhoneNumberProvider)


class FakeProfile:
    MIN_PWD_LEN = 6

    def __init__(self, username=None):
        self.username = username or fake.username()
        self.gender = random.choice(['M', 'F'])
        self.first_name = fake.first_name_male() if self.gender == 'M' else fake.first_name_female()
        self.last_name = fake.last_name()
        self.dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
        self.contact_email = f'{fake.username()}@{fake.free_email_domain()}'
        self.addr_state = fake.state_abbr()
        self.us_phone_number = fake.us_e164()
        self.password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

    def __str__(self):
        return f'FakeProfile -> username: {self.username}, full_name: {self.full_name}'

    @property
    def full_gender(self):
        return 'MALE' if self.gender == 'M' else 'FEMALE'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def dob_yyyymmdd(self):
        return self.dob.strftime('%Y-%m-%d')
