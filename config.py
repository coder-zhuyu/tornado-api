import os
import logging


class Config:
    debug = False
    cookie_secret = os.getenv('COOKIE_SECRET')

    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_schema = os.getenv('DB_SCHEMA')
    db_pool_minsize = os.getenv('DB_POOL_MINSIZE')
    db_pool_maxsize = os.getenv('DB_POOL_MAXSIZE')
    db_connect_timeout = os.getenv('DB_CONNECT_TIMEOUT')

    log_level = logging.INFO
    log_path = os.getenv('LOG_PATH')

    token_key = os.getenv('TOKEN_KEY')
    token_algorithm = os.getenv('TOKEN_ALGORITHM')
    token_exp_delta = os.getenv('TOKEN_EXP_DELTA')


class DevelopmentConfig(Config):
    # debug = True
    cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"

    db_host = '192.168.165.11'
    db_port = 3306
    db_user = 'root'
    db_password = 'Zhuyu!2017@'
    db_schema = 'metadata'
    db_pool_minsize = 50
    db_pool_maxsize = 100
    db_connect_timeout = 30

    log_level = logging.DEBUG
    log_path = './logs/api.log'

    token_key = '871c3acf-e6c5-4fae-b8be-acb9f5da18aa'
    token_algorithm = 'HS256'
    token_exp_delta = 3600      # seconds


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
