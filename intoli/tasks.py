import logging

from djstarter import decorators
from ua_parser import user_agent_parser

from intoli import intoli_api
from intoli.clients import IntoliClient
from intoli.exceptions import IntoliError
from intoli.models import Profile

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

        old_oids = list(Profile.objects.all_oids())
        profiles = self.build_profiles(r_profiles)

        try:
            new_profiles = Profile.objects.bulk_create(profiles)
        except Exception as e:
            raise IntoliError(info=f'Error adding user agents: {str(e)}')
        else:
            logger.info(f'Created New Intoli Profiles: {len(new_profiles)}')
            logger.info(f'Deleted Old Intoli Profiles: {Profile.objects.bulk_delete(oids=old_oids)[0]}')

    @staticmethod
    def build_profiles(r_profiles):
        new_profiles = list()
        for profile in r_profiles.valid_profiles:
            temp_profile = Profile(
                device_category=profile.device_category,
                platform=profile.platform,
                screen_height=profile.screen_height,
                screen_width=profile.screen_width,
                user_agent=profile.user_agent,
                viewport_height=profile.viewport_height,
                viewport_width=profile.viewport_width,
                weight=profile.weight,
            )
            print(temp_profile)
            new_profiles.append(
                temp_profile
            )
            ua_parser = user_agent_parser.Parse(profile.user_agent)
            print(f'ua_parser: {ua_parser}')
        return new_profiles
