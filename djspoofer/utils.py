import logging
import random

from faker import Faker
from ua_parser import user_agent_parser

from . import providers

logger = logging.getLogger(__name__)


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


class UserAgentParser:
    class UserAgent:
        def __init__(self, data):
            self.data = data

        @property
        def family(self):
            return self.data['family']

        @property
        def major(self):
            return self.data['major']

        @property
        def minor(self):
            return self.data['minor']

        @property
        def patch(self):
            return self.data['patch']

    class OS(UserAgent):
        pass

    def __init__(self, user_agent):
        self.ua_parser = user_agent_parser.Parse(user_agent)
        self._user_agent = self.UserAgent(self.ua_parser['user_agent'])
        self._os = self.OS(self.ua_parser['os'])

    @property
    def browser(self):
        return self._user_agent.family

    @property
    def browser_major_version(self):
        return self._user_agent.major

    @property
    def os(self):
        return self._os.family

    def __str__(self):
        return f'UserAgentParser -> {self.ua_parser}'


def proxy_dict(proxy_url):
    if proxy_url:
        return {
            'http://': proxy_url,
            'https://': proxy_url,
        }
    return dict()
