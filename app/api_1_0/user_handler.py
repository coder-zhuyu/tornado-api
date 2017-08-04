# -*- coding: utf-8 -*-
from ..db import Db
from ..request_handler import BaseRequestHandler, login_required
from ..log import debug_log, info_log, warning_log, error_log
from schema import Schema, Regex


class UserHandler(BaseRequestHandler):
    @login_required
    async def get(self, user_id):
        result = await Db.select_one("SELECT id, username, phone, email FROM user_admin where id=%s limit 1",
                                     int(user_id))
        debug_log(result)
        if result is None:
            self.response_json(code='600100')
        else:
            self.response_json(result=result)

    @login_required
    async def put(self, user_id):
        phone = self.get_argument('phone')
        name = self.get_argument('name')

        Regex(r'^1[0-9]{10}$').validate(phone)
        Schema(str).validate(name)

        affected_rows = await Db.update("UPDATE user_admin set phone=%s, name=%s where id=%s",
                                        (phone, name, int(user_id)))
        debug_log(affected_rows)
        if affected_rows is -1:
            self.response_json(code='600101')
        else:
            self.response_json()
