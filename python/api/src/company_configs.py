

_CONFIG = {
    'NAME': {
        'COMPANY': 'TopUp',
        'PRODUCT': 'TopUp',
        'KEY': 'company_topup',
    },
    'HOST': {
        'COMPANY': 'https://sample-topup.com',
        'PRODUCT': 'https://app.sample-topup.com',
    },
    'EMAIL': {
        'COMPANY': 'systemdemo99@gmail.com',
        'PRODUCT': 'systemdemo99@gmail.com',
        'DNR': 'systemdemo99@gmail.com',  # do not reply
    },
    'LOGO': {
        'COMPANY': {
            'DEF': 'PNG',
            'PNG': 'https://ui-avatars.com/api/?name=PS',
        },
        'PRODUCT': {
            'DEF': 'SVG',
            'SVG': 'https://ui-avatars.com/api/?name=PS',
        }
    }
}


_KEY = {
    'PUBLIC': 'public_saas',        # public saas
    'ORG': 'enterprise_saas',       # multi tenant enterprise saas
    'DEDICATED': 'dedicated_saas',  # isolated / dedicated enterprise saas
    'ONPREM': 'onprem_saas',        # on prem deployent
}


def _populate_config():
    global _CONFIG
    config = _CONFIG

    config['KEY'] = _KEY

    config['LOGO']['COMPANY']['ALT'] = config['NAME']['COMPANY']
    config['LOGO']['COMPANY']['IMG'] = config['LOGO']['COMPANY'][config['LOGO']['COMPANY']['DEF']]

    config['LOGO']['PRODUCT']['ALT'] = config['NAME']['PRODUCT']
    config['LOGO']['PRODUCT']['IMG'] = config['LOGO']['PRODUCT'][config['LOGO']['PRODUCT']['DEF']]

    return config


CONFIG = _populate_config()

print(CONFIG)
