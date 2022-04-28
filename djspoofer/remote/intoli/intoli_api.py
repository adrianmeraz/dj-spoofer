import gzip
import json
import logging
from io import BytesIO

from djstarter import decorators

from .exceptions import IntoliError

logger = logging.getLogger(__name__)

BASE_URL = 'https://raw.githubusercontent.com/intoli/user-agents/master/src/user-agents.json.gz'
UA_BAD_CHARS = '\"\''
UA_BLACKLIST = ('coc_coc_browser', 'QQBrowser', 'WeChat', 'YaBrowser', 'zh-CN', 'zh_CN', 'zhihu')
UA_LEN_RANGE = (40, 160)
DEVICE_CATEGORY_LEN_RANGE = (4, 16)
PLATFORM_LEN_RANGE = (4, 16)
MIN_WEIGHT = .0001


@decorators.wrap_exceptions(raise_as=IntoliError)
def get_profiles(client):
    params = {
        'format': 'json',
    }

    with client.stream('GET', BASE_URL, params=params) as response:
        json_io = BytesIO()
        try:
            for chunk in response.iter_bytes(chunk_size=8192):
                json_io.write(chunk)
                json_io.flush()
            json_io.seek(0)
            with gzip.GzipFile(fileobj=json_io, mode='rb') as gz_file:
                return GetProfilesResponse(json.load(gz_file))
        finally:
            json_io.close()


class GetProfilesResponse:
    def __init__(self, json_data):
        self.profiles = [IntoliProfile(profile) for profile in json_data]

    @property
    def valid_profiles(self):
        return [p for p in self.profiles if p.is_valid_profile]


class IntoliProfile:

    def __init__(self, data):
        self.device_category = data.get('deviceCategory')
        self.platform = data.get('platform')
        self.screen_height = data.get('screenHeight') or 1080
        self.screen_width = data.get('screenWidth') or 1920
        self.user_agent = data.get('userAgent').strip(UA_BAD_CHARS)
        self.viewport_height = data.get('viewportHeight') or 920
        self.viewport_width = data.get('viewportWidth') or 1415
        self.weight = data.get('weight')

    @property
    def is_valid_profile(self):
        return all([
            self.is_valid_user_agent,
            not self.is_user_agent_blacklisted,
            self.is_valid_device_category,
            self.is_valid_platform,
            self.is_valid_weight
        ])

    @property
    def is_valid_user_agent(self):
        return UA_LEN_RANGE[0] <= len(self.user_agent) <= UA_LEN_RANGE[1]

    @property
    def is_user_agent_blacklisted(self):
        return any(x.lower() in self.user_agent.lower() for x in UA_BLACKLIST)

    @property
    def is_valid_device_category(self):
        return DEVICE_CATEGORY_LEN_RANGE[0] <= len(self.device_category) <= DEVICE_CATEGORY_LEN_RANGE[1]

    @property
    def is_valid_platform(self):
        return PLATFORM_LEN_RANGE[0] <= len(self.platform) <= PLATFORM_LEN_RANGE[1]

    @property
    def is_valid_weight(self):
        return self.weight > MIN_WEIGHT
