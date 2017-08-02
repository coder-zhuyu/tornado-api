import os
import logging


class Config:
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_schema = os.getenv('DB_SCHEMA')
    db_pool_minsize = os.getenv('DB_POOL_MINSIZE')
    db_pool_maxsize = os.getenv('DB_POOL_MAXSIZE')
    db_connect_timeout = os.getenv('DB_CONNECT_TIMEOUT')

    logging.getLogger('tornado.application').setLevel(logging.INFO)


class DevelopmentConfig(Config):

    db_host = '10.0.32.34'
    db_port = 3306
    db_user = 'root'
    db_password = '111111'
    db_schema = 'api'
    db_pool_minsize = 50
    db_pool_maxsize = 100
    db_connect_timeout = 30

    logging.getLogger('tornado.application').setLevel(logging.DEBUG)


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}


def get_config_name():
    if os.getenv('ENV').startswith('{{'):
        return 'default'
    else:
        return os.getenv('ENV')


def get_config():
    return _config[get_config_name()]


config = get_config()
