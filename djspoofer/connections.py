import logging

import h2
from h2.settings import Settings, SettingCodes
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
    self._h2_state.local_settings = build_h2_settings(get_h2_frame_fingerprint())

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
        psuedo_header_order='p,m,a,s'   # TODO Implement psuedo header order
    )


def build_h2_settings(h2_settings_fingerprint):
    h2_fp = h2_settings_fingerprint
    initial_values = {
        SettingCodes.HEADER_TABLE_SIZE: h2_fp.header_table_size,                            # 1 (Required)
        SettingCodes.ENABLE_PUSH: int(h2_fp.enable_push) if h2_fp.enable_push else None,    # 2 (Required)
        SettingCodes.MAX_CONCURRENT_STREAMS: h2_fp.max_concurrent_streams,                  # 3 (Optional)
        SettingCodes.INITIAL_WINDOW_SIZE: h2_fp.initial_window_size,                        # 4 (Required)
        SettingCodes.MAX_FRAME_SIZE: h2_fp.max_frame_size,                                  # 5 (Required)
        SettingCodes.MAX_HEADER_LIST_SIZE: h2_fp.max_header_list_size,                      # 6 (Optional)
    }
    initial_values = {k: v for k, v in initial_values.items() if v}
    return h2.settings.Settings(
        client=True,
        initial_values=initial_values,
    )
