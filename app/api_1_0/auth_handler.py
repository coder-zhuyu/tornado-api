# -*- coding: utf-8 -*-
from ..db import Db
from ..request_handler import BaseRequestHandler, login_required
from ..log import debug_log, info_log, warning_log, error_log
from schema import Schema, Regex
import concurrent.futures
import bcrypt
import tornado
import tornado.escape
import tornado.web
import asyncio

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class AuthLoginHandler(BaseRequestHandler):
    """Auth login."""
    async def post(self):
        user_name = self.get_argument('username')
        password = self.get_argument('password')

        Schema(str).validate(user_name)
        Schema(str).validate((password))

        result = await Db.select_one("SELECT * FROM user_admin where username=%s limit 1", user_name)
        debug_log(result)
        if not result:
            self.response_json(code='401001')
            return

        # check password
        job = executor.submit(bcrypt.hashpw, tornado.escape.utf8(password), tornado.escape.utf8(result['password_hash']))
        hashed_password = tornado.escape.to_unicode(await asyncio.wrap_future(job))

        if hashed_password == result['password_hash']:
            self.set_secure_cookie('user', str(result['id']))
            self.response_json()
        else:
            self.response_json(code='401001')


class AuthLogoutHandler(BaseRequestHandler):
    """Auth logout."""
    @login_required
    async def get(self):
        # clear cookie
        self.clear_cookie('user')
        current_user = await self.get_current_user()
        debug_log(current_user)
        self.response_json()
