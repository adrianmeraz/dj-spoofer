from djstarter import utils as core_utils

BROWSER_REFRESH_MSG = 'Browser will refresh periodically to display the status.'


class ProxyModes(core_utils.ChoiceEnum):
    ROTATING = 0
    STICKY = 1
    GENERAL = 2
