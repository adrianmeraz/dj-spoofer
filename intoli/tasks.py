import logging

from intoli import intoli_api
from intoli.clients import IntoliClient
from intoli.exceptions import IntoliError
from intoli.models import Profile

from djstarter import decorators

logger = logging.getLogger(__name__)


@decorators.db_conn_close
def get_profiles(*args, **kwargs):
    GetProfiles(*args, **kwargs).start()


class GetProfiles:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        with IntoliClient() as i_client:
            r_profiles = intoli_api.get_profiles(i_client)

        old_oids = self.get_old_profile_oids()
        new_profiles = self.build_profiles(r_profiles)

        try:
            Profile.objects.bulk_create(new_profiles)
        except Exception as e:
            raise IntoliError(info=f'Error adding user agents: {str(e)}')
        else:
            logger.info(f'Deleted Old Intoli Profiles: {Profile.objects.bulk_delete(oids=old_oids)[0]}')

    @staticmethod
    def build_profiles(r_profiles):
        new_profiles = list()
        for profile in r_profiles.valid_profiles:
            new_profiles.append(
                Profile(
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
        logger.info(f'New Intoli Profiles: {len(new_profiles)}')
        return new_profiles

    @staticmethod
    def get_old_profile_oids():
        oids = Profile.objects.all_oids()
        logger.info(f'Old Intoli Profiles: {len(oids)}')
        return oids
