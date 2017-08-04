# -*- coding: utf-8 -*-
from tornado.web import RequestHandler
from .codemsg import CodeMsg
import json
from .db import Db
from .log import debug_log, info_log, warning_log, error_log
from functools import wraps


class BaseRequestHandler(RequestHandler):
    """Base class for HTTP request handlers.

    Override the method get_current_user in coroutine.
    Add a method response_json for HTTP json response.
    """
    async def get_current_user(self):
        """Override to determine the current user from, e.g., a cookie."""
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        result = await Db.select_one("SELECT * FROM user_admin where id=%s limit 1",
                                     int(user_id))
        debug_log(result)
        return result

    def response_json(self, result=None, code='000000', status=200):
        """HTTP response in the form of json.

        :param result: return body
        :param code: return code
        :param status: http status
        :return:
        """
        resp_dict = {
            'code': code,
            'msg': CodeMsg.get_msg(code)
        }

        if result is not None:
            resp_dict['result'] = result

        self.set_status(status)
        self.set_header('Content-Type', 'application/json; charset=utf-8')

        self.write(json.dumps(resp_dict, ensure_ascii=False))


def login_required(f):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, return 401.
    """
    @wraps(f)
    async def decorated_function(self, *args, **kwargs):
        current_user = await self.get_current_user()
        if not current_user:
            self.response_json(code='401000', status=401)
            return
        return await f(self, *args, **kwargs)

    return decorated_function
