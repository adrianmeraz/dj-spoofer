import ssl

from djstarter import utils as core_utils


class ProxyModes(core_utils.ChoiceEnum):
    GENERAL = 10
    ROTATING = 20
    STICKY = 30


class Ciphers:
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
    ssl.OP_CIPHER_SERVER_PREFERENCE,
    ssl.OP_SINGLE_DH_USE,
    ssl.OP_SINGLE_ECDH_USE,
    ssl.OP_NO_COMPRESSION,
    ssl.OP_NO_TICKET,
    ssl.OP_NO_RENEGOTIATION,
    ssl.OP_ENABLE_MIDDLEBOX_COMPAT,
]

SUPPORTED_OS_BROWSER_MAP = {
    'Windows': [
        'Chrome',
        'Edge',
        'Firefox'
    ],
    'Linux': [
        'Chrome',
        'Firefox'
    ],
    'iOS': [
        'Chrome',
        'Safari',
    ]
}
