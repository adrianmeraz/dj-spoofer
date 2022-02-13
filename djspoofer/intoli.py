import gzip
import json
import logging
from io import BytesIO
from json.decoder import JSONDecodeError

from httpx import RequestError

from . import exceptions

logger = logging.getLogger(__name__)
retry_exceptions = (RequestError, JSONDecodeError)

UA_BAD_CHARS = '\"\''
UA_BLACKLIST = ('coc_coc_browser', 'QQBrowser', 'WeChat', 'YaBrowser', 'zh-CN', 'zhihu')
UA_MIN_LEN = 40
UA_MAX_LEN = 160


def is_valid_profile(profile):
    if not UA_MIN_LEN < len(profile.user_agent) < UA_MAX_LEN:
        return False
    elif any(x.lower() in profile.user_agent.lower() for x in UA_BLACKLIST):
        return False
    elif len(profile.device_category) > 16:
        return False
    elif len(profile.platform) > 16:
        return False
    else:
        return True


def get_profiles(s_client):
    url = 'https://raw.githubusercontent.com/intoli/user-agents/master/src/user-agents.json.gz'

    params = {
        'format': 'json',
    }

    with s_client.stream('GET', url, params=params) as response:
        if response.status_code >= 500:
            response.raise_for_status()
        if response.is_error:
            raise exceptions.DJSpooferError(info=f'Problem getting file at url: {url}')

        json_io = BytesIO()
        try:
            for chunk in response.iter_bytes(chunk_size=8192):
                json_io.write(chunk)
                json_io.flush()
            json_io.seek(0)
            with gzip.GzipFile(fileobj=json_io, mode='rb') as gz_file:
                raw_json = json.load(gz_file)
                raw_profiles = [IntoliProfile(profile) for profile in raw_json]
                logger.info(f'Number of Raw Intoli Profiles: {len(raw_profiles)}')
                return [p for p in raw_profiles if is_valid_profile(p)]
        finally:
            json_io.close()


class IntoliProfile:
    def __init__(self, js):
        self.device_category = js.get('deviceCategory')
        self.platform = js.get('platform')
        self.screen_height = js.get('screenHeight') or 1080
        self.screen_width = js.get('screenWidth') or 1920
        self.user_agent = js.get('userAgent').strip(UA_BAD_CHARS)
        self.viewport_height = js.get('viewportHeight') or 920
        self.viewport_width = js.get('viewportWidth') or 1415
        self.weight = js.get('weight')