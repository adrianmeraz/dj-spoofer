import logging
from json import JSONDecodeError

from httpx import Client, RequestError
from urllib3.exceptions import HTTPError

from djspoofer import exceptions
from . import models, intoli

logger = logging.getLogger(__name__)

_warn_exceptions = (
    exceptions.ApiError,
    JSONDecodeError,
    RequestError,
    HTTPError
)


def get_profiles(*args, **kwargs):
    GetProfiles(*args, **kwargs).start()


class GetProfiles:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def start():
        with Client() as client:
            profiles = intoli.get_profiles(client)
        new_profiles = []

        for profile in profiles:
            new_profiles.append(
                models.Profile(
                    device_category=profile.device_category,
                    platform=profile.platform,
                    screen_height=profile.screen_height,
                    screen_width=profile.screen_width,
                    user_agent=profile.user_agent,
                    viewport_height=profile.viewport_height,
                    viewport_width=profile.viewport_width,
                    weight=profile.weight,
                )
            )

        logger.info(f'Got {len(new_profiles)} New Intoli Profiles')
        try:
            models.Profile.objects.bulk_create(new_profiles)
        except Exception as e:
            raise exceptions.AppError(info=f'Error adding user agents: {str(e)}')
        else:
            logger.info(f'Deleted {models.Profile.objects.older_than_n_minutes().delete()[0]} Old Intoli Profiles')
