# -*- coding: utf-8 -*-
# Created by coder-zhuyu on 2018/9/7
"""
"""
import tornado.web
from config import config


settings = dict(
    # cookie_secret=config.cookie_secret,
    debug=config.debug
)


class RouterConfig(tornado.web.Application):
    """ 重置Tornado自带的路有对象 """

    def route(self, url):
        """
        :param url: URL地址
        :return: 注册路由关系对应表的装饰器
        """

        def register(handler):
            """
            :param handler: URL对应的Handler
            :return: Handler
            """
            self.add_handlers(".*$", [(url, handler)])  # URL和Handler对应关系添加到路由表中
            return handler

        return register


app = RouterConfig(**settings)  # 创建Tornado路由对象，默认路由表为空
