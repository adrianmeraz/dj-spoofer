import logging

from djspoofer.exceptions import DJSpooferError
from intoli import intoli_api
from intoli.clients import IntoliClient
from . import models

logger = logging.getLogger(__name__)


def get_profiles(*args, **kwargs):
    GetProfiles(*args, **kwargs).start()


class GetProfiles:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def start():
        with IntoliClient() as i_client:
            profiles = intoli_api.get_profiles(i_client)
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
            raise DJSpooferError(info=f'Error adding user agents: {str(e)}')
        else:
            logger.info(f'Deleted {models.Profile.objects.older_than_n_minutes().delete()[0]} Old Intoli Profiles')
