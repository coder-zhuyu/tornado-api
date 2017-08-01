# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
from .codemsg import CodeMsg
import json


class BaseRequestHandler(RequestHandler):

    def response_json(self, result=None, code='000000', status=200):
        resp_dict = {
            'code': code,
            'msg': CodeMsg.get_msg(code)
        }

        if result is not None:
            resp_dict['result'] = result

        self.set_status(status)
        self.set_header('Content-Type', 'application/json; charset=utf-8')

        self.write(json.dumps(resp_dict, ensure_ascii=False))
