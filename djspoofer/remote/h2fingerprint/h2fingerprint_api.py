import logging

from django.conf import settings
from djstarter import decorators

from .exceptions import H2Error

logger = logging.getLogger(__name__)


BASE_URL = settings.H2_FINGERPRINT_API_BASE_URL


@decorators.wrap_exceptions(raise_as=H2Error)
def get_h2_fingerprint(client, *args, **kwargs):
    url = f'{BASE_URL}'
    r = client.get(url, *args, **kwargs)
    r.raise_for_status()
    return H2FingerprintResponse(r.json())


class H2FingerprintResponse:

    class SettingsFrame:
        def __init__(self, data):
            self.data = data
            pairs = [pair.split(':') for pair in data.split(';')]
            kv_map = {str(k): v for k, v in pairs}
            self.header_table_size = kv_map.get('1')
            self.push_enabled = kv_map.get('2')
            self.max_concurrent_streams = kv_map.get('3')
            self.initial_window_size = kv_map.get('4')
            self.max_frame_size = kv_map.get('5')
            self.max_header_list_size = kv_map.get('6')

    class WindowFrame:
        def __init__(self, data):
            self.window_update_increment = data

    class PriorityFrame:
        def __init__(self, data):
            parts = [v for v in data.split(':')]
            self.stream_id = parts[0]
            self.is_exclusive = parts[1]
            self.depends_on_id = parts[2]
            self.weight = parts[3]

    def __init__(self, data):
        self.fingerprint = data['fingerprint']
        self.settings_frame = self.SettingsFrame(data['settings_frame'])
        self.window_frame = self.WindowFrame(data['window_frame'])
        self.priority_frame = self.PriorityFrame(data['priority_frame'])
        self.pseudo_headers = data['pseudo_headers']

