# -*- coding: utf-8 -*-
import tornado.web
from .api_1_0 import UserHandler


def create_app():
    app = tornado.web.Application([
        ("/user/([0-9]+)", UserHandler),
    ])

    return app
