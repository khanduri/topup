# -*- coding: utf-8 -*-
import os

from src import create_app
app = create_app()


def _print_config_variable():

    environ_vars = [
        'APP_SETTINGS',
        'TARGET_SUB_DOMAIN',
    ]
    config_vars = [
        'DEBUG',
    ]

    # We don't want to print out the raw connection string in PROD
    if os.environ['APP_SETTINGS'] != 'config.LiveConfig':
        config_vars.append('SQLALCHEMY_DATABASE_URI')
        config_vars.append('MONGO_URI')

    environ_vars = tuple(environ_vars)
    config_vars = tuple(config_vars)

    mapper = {
        environ_vars: os.environ,
        config_vars: app.config,
    }

    app.logger.info('---- START: Configs ----')
    for _vars in mapper:
        for _var in _vars:
            app.logger.info(" - {}: {}".format(_var, mapper[_vars][_var]))
    app.logger.info('---- END: Configs ----')
    app.logger.info("APP_SETTINGS -->> {} <<-- : Printing this from app/log.py.".format(os.environ['APP_SETTINGS']))


_print_config_variable()
