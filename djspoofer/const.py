from djstarter import utils as core_utils


class ProxyModes(core_utils.ChoiceEnum):
    GENERAL = 10
    ROTATING = 20
    STICKY = 30
