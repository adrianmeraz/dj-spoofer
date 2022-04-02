import logging

from djstarter.clients import Http2Client

logger = logging.getLogger(__name__)


class IntoliClient(Http2Client):
    """
    Intoli Http Client
    """
