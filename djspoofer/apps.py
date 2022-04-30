import logging
from django.apps import AppConfig
from h2.connection import H2Connection

logger = logging.getLogger(__name__)


class DJSpooferConfig(AppConfig):
    name = 'djspoofer'
    verbose_name = 'DJ Spoofer App'

    def ready(self):
        from httpcore._sync.http2 import HTTP2Connection
        from djspoofer import connections

        # Monkey patching to allow for dynamic h2 settings frame
        HTTP2Connection._send_connection_init = connections._send_connection_init
        logger.debug('Monkey patched HTTP2Connection._send_connection_init')
