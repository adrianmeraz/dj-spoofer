from ssl import Options

from djstarter import utils as core_utils


class ProxyModes(core_utils.ChoiceEnum):
    GENERAL = 10
    ROTATING = 20
    STICKY = 30


class Clients(core_utils.ChoiceEnum):
    GENERIC = 5
    CHROME_DESKTOP = 20
    FIREFOX_DESKTOP = 30


class Ciphers(core_utils.ChoiceEnum):
    TLS_AES_128_GCM_SHA256 = 'AES128-GCM-SHA256'
    TLS_CHACHA20_POLY1305_SHA256 = 'CHACHA20-POLY1305-SHA256'
    TLS_AES_256_GCM_SHA384 = 'AES256-GCM-SHA384'
    TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 = 'ECDHE-ECDSA-AES128-GCM-SHA256'
    TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 = 'ECDHE-RSA-AES128-GCM-SHA256'
    TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 = 'ECDHE-ECDSA-CHACHA20-POLY1305'
    TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 = 'ECDHE-RSA-CHACHA20-POLY1305'
    TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 = 'ECDHE-ECDSA-AES256-GCM-SHA384'
    TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 = 'ECDHE-RSA-AES256-GCM-SHA384'
    TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA = 'ECDHE-ECDSA-AES256-SHA'
    TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA = 'ECDHE-ECDSA-AES128-SHA'
    TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA = 'ECDHE-RSA-AES128-SHA'
    TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA = 'ECDHE-RSA-AES256-SHA'
    TLS_RSA_WITH_AES_128_GCM_SHA256 = 'AES128-GCM-SHA256'
    TLS_RSA_WITH_AES_256_GCM_SHA384 = 'AES256-GCM-SHA384'
    TLS_RSA_WITH_AES_128_CBC_SHA = 'AES128-SHA'
    TLS_RSA_WITH_AES_256_CBC_SHA = 'AES256-SHA'


ChromeDesktopCiphers = [
    Ciphers.TLS_AES_128_GCM_SHA256,
    Ciphers.TLS_AES_256_GCM_SHA384,
    Ciphers.TLS_CHACHA20_POLY1305_SHA256,
    Ciphers.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
    Ciphers.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
    Ciphers.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
    Ciphers.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
    Ciphers.TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,
    Ciphers.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,
    Ciphers.TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,
    Ciphers.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,
    Ciphers.TLS_RSA_WITH_AES_128_GCM_SHA256,
    Ciphers.TLS_RSA_WITH_AES_256_GCM_SHA384,
    Ciphers.TLS_RSA_WITH_AES_128_CBC_SHA,
    Ciphers.TLS_RSA_WITH_AES_256_CBC_SHA,
]

FirefoxDesktopCiphers = [
    Ciphers.TLS_AES_128_GCM_SHA256,
    Ciphers.TLS_CHACHA20_POLY1305_SHA256,
    Ciphers.TLS_AES_256_GCM_SHA384,
    Ciphers.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
    Ciphers.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
    Ciphers.TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,
    Ciphers.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,
    Ciphers.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
    Ciphers.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
    Ciphers.TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
    Ciphers.TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,
    Ciphers.TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,
    Ciphers.TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,
    Ciphers.TLS_RSA_WITH_AES_128_GCM_SHA256,
    Ciphers.TLS_RSA_WITH_AES_256_GCM_SHA384,
    Ciphers.TLS_RSA_WITH_AES_128_CBC_SHA,
]

TLS_EXTENSIONS = [
    Options.OP_CIPHER_SERVER_PREFERENCE,
    Options.OP_SINGLE_DH_USE,
    Options.OP_SINGLE_ECDH_USE,
    Options.OP_NO_COMPRESSION,
    Options.OP_NO_TICKET,
    Options.OP_NO_RENEGOTIATION,
    Options.OP_ENABLE_MIDDLEBOX_COMPAT,
]

