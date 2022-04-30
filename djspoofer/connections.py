import logging

import h2
from h2.settings import Settings
from httpcore._models import Request
from httpcore._sync.http2 import HTTP2Connection
from djspoofer import utils
from djspoofer.models import H2FrameFingerprint

logger = logging.getLogger(__name__)


def _send_connection_init(self, request: Request) -> None:
    """
        The HTTP/2 connection requires some initial setup before we can start
        using individual request/response streams on it.
    """
    # Need to set these manually here instead of manipulating via
    # __setitem__() otherwise the H2Connection will emit SettingsUpdate
    # frames in addition to sending the undesired defaults.

    self._h2_state.local_settings = h2.settings.Settings(
        client=True,
        initial_values={
            # Disable PUSH_PROMISE frames from the server since we don't do anything
            # with them for now.  Maybe when we support caching?
            h2.settings.SettingCodes.HEADER_TABLE_SIZE: 65536,
            h2.settings.SettingCodes.ENABLE_PUSH: 0,
            # These two are taken from h2 for safe defaults
            h2.settings.SettingCodes.MAX_CONCURRENT_STREAMS: 1000,
            h2.settings.SettingCodes.MAX_HEADER_LIST_SIZE: 65536,
        },
    )

    # Some websites (*cough* Yahoo *cough*) balk at this setting being
    # present in the initial handshake since it's not defined in the original
    # RFC despite the RFC mandating ignoring settings you don't know about.
    del self._h2_state.local_settings[
        h2.settings.SettingCodes.ENABLE_CONNECT_PROTOCOL
    ]

    self._h2_state.initiate_connection()
    self._h2_state.increment_flow_control_window(2 ** 24)
    self._write_outgoing_data(request)


def get_h2_frame_fingerprint(request):
    user_agent = request.headers['user-agent']
    ua_parser = utils.UserAgentParser(user_agent)
    # TODO Pull H2FrameFingerprint record using os and browser

    return H2FrameFingerprint(
        header_table_size=4096,
        enable_push=True,

    )


# Monkey patching to allow for dynamic h2 settings frame
HTTP2Connection._send_connection_init = _send_connection_init
