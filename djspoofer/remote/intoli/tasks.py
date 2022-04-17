import logging

from djstarter import decorators
from djstarter.clients import Http2Client

from djspoofer import utils as s_utils
from djspoofer.remote.intoli import intoli_api
from djspoofer.remote.intoli.exceptions import IntoliError
from djspoofer.models import Profile

logger = logging.getLogger(__name__)


@decorators.db_conn_close
def get_profiles(*args, **kwargs):
    GetProfiles(*args, **kwargs).start()


class GetProfiles:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        with Http2Client() as client:
            r_profiles = intoli_api.get_profiles(client)

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
            ua_parser = s_utils.UserAgentParser(profile.user_agent)
            temp_profile = Profile(
                browser=ua_parser.browser,
                device_category=profile.device_category,
                os=ua_parser.os,
                platform=profile.platform,
                screen_height=profile.screen_height,
                screen_width=profile.screen_width,
                user_agent=profile.user_agent,
                viewport_height=profile.viewport_height,
                viewport_width=profile.viewport_width,
                weight=profile.weight,
            )
            new_profiles.append(temp_profile)
            # print(f'{temp_profile}\n{ua_parser}\n')
        return new_profiles
