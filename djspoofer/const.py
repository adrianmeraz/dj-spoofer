from djstarter import utils as core_utils


class ProxyModes(core_utils.ChoiceEnum):
    ROTATING = 0
    STICKY = 1
    GENERAL = 2
