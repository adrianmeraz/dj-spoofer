import logging
import time
from urllib.parse import urlparse

from django.conf import settings
from djstarter import decorators

from .exceptions import CaptchaUnsolvable, CriticalError, TwoCaptchaError, CaptchaNotReady, InvalidResponse

logger = logging.getLogger(__name__)

API_KEY = settings.TWO_CAPTCHA_API_KEY
BASE_URL = settings.TWO_CAPTCHA_BASE_URL

SOLVE_ERRORS = (
    'ERROR_CAPTCHA_UNSOLVABLE',
)
WARN_ERRORS = (
    'ERROR_WRONG_CAPTCHA_ID',
    'MAX_USER_TURN',
    'ERROR_NO_SLOT_AVAILABLE',
)
CRITICAL_ERRORS = (
    'ERROR_WRONG_USER_KEY',
    'ERROR_KEY_DOES_NOT_EXIST',
    'ERROR_ZERO_BALANCE',
    'IP_BANNED',
    'ERROR_GOOGLEKEY',
)


class TwoCaptchaInfo:
    def __init__(self, data):
        self.status = data['status']
        self.request = data['request']

    @property
    def bad_captcha_reported(self):
        return self.request == 'OK_REPORT_RECORDED'


class SolvedTokenResp:
    def __init__(self, g_token, captcha_id):
        self.g_token = g_token
        self.captcha_id = captcha_id


def captcha_error_check(r_info, captcha_id):
    if r_info.status != 1:
        raise InvalidResponse(f'Captcha ID: {captcha_id}')
    exc_map = {
        'ERROR_WRONG_CAPTCHA_ID': TwoCaptchaError,
        'MAX_USER_TURN': TwoCaptchaError,
        'ERROR_NO_SLOT_AVAILABLE': TwoCaptchaError,
        'ERROR_WRONG_USER_KEY': CriticalError,
        'ERROR_KEY_DOES_NOT_EXIST': CriticalError,
        'ERROR_ZERO_BALANCE': CriticalError,
        'IP_BANNED': CriticalError,
        'ERROR_GOOGLEKEY': CriticalError,
        'ERROR_CAPTCHA_UNSOLVABLE': CaptchaUnsolvable,
        'CAPCHA_NOT_READY':  CaptchaNotReady
    }
    if exc := exc_map.get(r_info.request):
        raise exc(f'Captcha ID: {captcha_id}')


@decorators.retry(retry_exceptions=CaptchaUnsolvable, tries=3, delay=0, backoff=0)
def get_solved_gcaptcha_info(client, proxy, sitekey, page_url):
    captcha_id = get_captcha_id(client=client, proxy=proxy, sitekey=sitekey, page_url=page_url)
    try:
        return get_solve_token(session=client, captcha_id=captcha_id)
    except Exception:
        report_bad_captcha(captcha_id)
        raise CaptchaUnsolvable(f'Captcha ID: {captcha_id}')


@decorators.retry(retry_exceptions=(CaptchaNotReady,), tries=60, delay=5, backoff=1)
def get_captcha_id(client, proxy, sitekey, page_url):
    url = f'{BASE_URL}/in.php'
    proxy_type = urlparse(proxy).scheme.upper()

    params = (
        ('key', API_KEY),
        ('method', 'userrecaptcha'),
        ('googlekey', sitekey),
        ('pageurl', page_url),
        ('json', '1'),
        ('proxy', proxy),
        ('proxytype', proxy_type)
    )
    data = {
        'proxy': proxy,
        'proxytype': proxy_type
    }

    r = client.post(url, params=params, data=data, allow_redirects=False)  # Disable redirects to network splash pages
    # Fail fast as each attempt costs a captcha solve
    if not r.status_code == 200:
        raise TwoCaptchaError(f'Cannot solve captcha with proxy "{proxy}" - Response: {r.text}')

    tc_info = TwoCaptchaInfo(r.json())
    captcha_error_check(tc_info, captcha_id=tc_info.request)
    return tc_info.request


@decorators.retry(retry_exceptions=(CaptchaNotReady,), tries=60, delay=5, backoff=1)
def get_solve_token(client, captcha_id):
    url = f'{BASE_URL}/res.php'
    params = (
        ('key', API_KEY),
        ('action', 'get'),
        ('id', captcha_id),
        ('json', 1),
    )

    r = client.get(url, params=params)

    r_info = TwoCaptchaInfo(r.json())
    captcha_error_check(r_info, captcha_id=captcha_id)
    return SolvedTokenResp(r_info.request, captcha_id)


@decorators.retry(retry_exceptions=(CaptchaNotReady,), tries=60, delay=5, backoff=1)
def report_bad_captcha(client, captcha_id):
    url = f'{BASE_URL}/res.php'
    params = (
        ('key', API_KEY),
        ('action', 'reportbad'),
        ('id', captcha_id),
        ('json', '1'),
    )

    r = client.get(url, params=params)

    tc_info = TwoCaptchaInfo(r.json())
    if tc_info.bad_captcha_reported:
        logger.info(f'Reported bad captcha id: {captcha_id}')
    else:
        raise TwoCaptchaError(f'Problem while reporting bad captcha: {r.text}')
