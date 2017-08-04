# -*- coding: utf-8 -*-
import tornado.web
from config import config
from .api_1_0 import UserHandler, AuthLoginHandler, AuthLogoutHandler


def create_app():
    settings = dict(
        cookie_secret=config.cookie_secret,
        debug=config.debug
    )

    handlers = [
        ("/user/([0-9]+)", UserHandler),
        ("/auth/login", AuthLoginHandler),
        ("/auth/logout", AuthLogoutHandler),
    ]

    app = tornado.web.Application(handlers, **settings)

    return app
