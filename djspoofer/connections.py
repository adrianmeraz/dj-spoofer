import logging

import h2
import time
from h2.settings import Settings, SettingCodes
from httpcore._sync import http2
from httpcore._models import Request

from djspoofer.models import H2SettingsFingerprint

logger = logging.getLogger(__name__)


def _send_connection_init(self, request: Request) -> None:
    """
        ** Monkey Patched in apps.py **
        The HTTP/2 connection requires some initial setup before we can start
        using individual request/response streams on it.
    """
    # Need to set these manually here instead of manipulating via
    # __setitem__() otherwise the H2Connection will emit SettingsUpdate
    # frames in addition to sending the undesired defaults.
    h2_frame_fingerprint = get_h2_fingerprint()
    self._h2_state.local_settings = build_h2_settings(h2_frame_fingerprint)

    # Some websites (*cough* Yahoo *cough*) balk at this setting being
    # present in the initial handshake since it's not defined in the original
    # RFC despite the RFC mandating ignoring settings you don't know about.
    del self._h2_state.local_settings[
        h2.settings.SettingCodes.ENABLE_CONNECT_PROTOCOL
    ]

    self._h2_state.get_next_available_stream_id = lambda: 7
    self._h2_state.initiate_connection()
    self._h2_state.increment_flow_control_window(h2_frame_fingerprint.window_update_increment)

    self._write_outgoing_data(request)


def _send_request_headers(self, request: Request, stream_id: int) -> None:
    """
        ** Monkey Patched in apps.py **
    """
    end_stream = not http2.has_body_headers(request)

    h2_fingerprint = get_h2_fingerprint()
    headers = get_psuedo_headers(request, h2_fingerprint=h2_fingerprint) + [
        (k.lower(), v)
        for k, v in request.headers
        if k.lower()
        not in (
            b"host",
            b"transfer-encoding",
        )
    ]

    self._h2_state.send_headers(
        stream_id,
        headers,
        end_stream=end_stream,
        priority_weight=201,
        priority_depends_on=0,
        priority_exclusive=False
    )
    self._h2_state.increment_flow_control_window(h2_fingerprint.window_update_increment, stream_id=stream_id)
    self._write_outgoing_data(request)


def get_psuedo_headers(request, h2_fingerprint):
    header_map = {
        'm': (b":method", request.method),
        'a': (b":authority", get_authority(request)),
        's': (b":scheme", request.url.scheme),
        'p': (b":path", request.url.target),
    }
    return [header_map[k] for k in h2_fingerprint.psuedo_header_order.split(',')]


def get_authority(request):
    """
        In HTTP/2 the ':authority' pseudo-header is used instead of 'Host'.
        In order to gracefully handle HTTP/1.1 and HTTP/2 we always require
        HTTP/1.1 style headers, and map them appropriately if we end up on
        an HTTP/2 connection.
    """
    return [v for k, v in request.headers if k.lower() == b"host"][0]


def get_h2_fingerprint():
    # TODO Pull real h2 fingerprints and add priority fields

    return H2SettingsFingerprint(
        header_table_size=4096,
        enable_push=True,
        max_concurrent_streams=1024,
        initial_window_size=32768,
        max_frame_size=16384,
        max_header_list_size=131072,
        psuedo_header_order='a,m,p,s',
        window_update_increment=2**24
    )


def build_h2_settings(h2_settings_fingerprint):
    # TODO Figure out how to omit some fields
    h2_fp = h2_settings_fingerprint
    initial_values = {
        SettingCodes.HEADER_TABLE_SIZE: h2_fp.header_table_size,                            # 0x01 (Required)
        SettingCodes.ENABLE_PUSH: int(h2_fp.enable_push) if h2_fp.enable_push else None,    # 0x02 (Required)
        SettingCodes.MAX_CONCURRENT_STREAMS: h2_fp.max_concurrent_streams,                  # 0x03 (Optional)
        SettingCodes.INITIAL_WINDOW_SIZE: h2_fp.initial_window_size,                        # 0x04 (Required)
        SettingCodes.MAX_FRAME_SIZE: h2_fp.max_frame_size,                                  # 0x05 (Required)
        SettingCodes.MAX_HEADER_LIST_SIZE: h2_fp.max_header_list_size,                      # 0x06 (Optional)
    }
    initial_values = {k: v for k, v in initial_values.items() if v}
    return h2.settings.Settings(
        client=True,
        initial_values=initial_values,
    )
