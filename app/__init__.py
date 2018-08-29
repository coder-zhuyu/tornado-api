# -*- coding: utf-8 -*-
import tornado.web
from config import config
from .log import init_log
from .api_1_0 import UserHandler, AuthLoginHandler, AuthLogoutHandler


def create_app():
    settings = dict(
        cookie_secret=config.cookie_secret,
        debug=config.debug
    )

    init_log(config.log_path, config.log_level)

    handlers = [
        ("/user/([0-9]+)", UserHandler),
        ("/auth/login", AuthLoginHandler),
        ("/auth/logout", AuthLogoutHandler),
    ]

    app = tornado.web.Application(handlers, **settings)

    return app
