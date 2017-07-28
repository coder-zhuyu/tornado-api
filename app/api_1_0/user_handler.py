# -*- coding: utf-8 -*-
from ..db import get_db_pool
from ..request_handler import BaseRequestHandler
from ..log import debug_log, info_log, warning_log, error_log


class UserHandler(BaseRequestHandler):
    async def get(self, user_id):
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT id, username, phone, email FROM user_admin where id=%d" % int(user_id))
                result = await cur.fetchall()
                info_log(result)

        self.response_json(result=result)
