import logging

import h2
from h2.settings import Settings
from httpcore._models import Request

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
    h2_frame_fingerprint = get_h2_frame_fingerprint()
    self._h2_state.local_settings = h2.settings.Settings(
        client=True,
        initial_values={
            h2.settings.SettingCodes.HEADER_TABLE_SIZE: h2_frame_fingerprint.header_table_size,
            h2.settings.SettingCodes.ENABLE_PUSH: int(h2_frame_fingerprint.enable_push),
            h2.settings.SettingCodes.MAX_CONCURRENT_STREAMS: h2_frame_fingerprint.max_concurrent_streams,
            h2.settings.SettingCodes.INITIAL_WINDOW_SIZE: h2_frame_fingerprint.initial_window_size,
            h2.settings.SettingCodes.MAX_FRAME_SIZE: h2_frame_fingerprint.max_frame_size,
            h2.settings.SettingCodes.MAX_HEADER_LIST_SIZE: h2_frame_fingerprint.max_header_list_size,
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


def get_h2_frame_fingerprint():
    # TODO Pull H2FrameFingerprint record using os and browser

    return H2FrameFingerprint(
        header_table_size=4096,
        enable_push=True,
        max_concurrent_streams=1024,
        initial_window_size=32768,
        max_frame_size=16384,
        max_header_list_size=131072,
        psuedo_header_order='p,m,a,s'
    )
