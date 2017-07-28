# -*- coding: utf-8 -*-
import aiomysql
from config import config


async def get_db_pool():
    pool = await aiomysql.create_pool(
        host=config.db_host,
        port=config.db_port,
        user=config.db_user,
        password=config.db_password,
        db=config.db_schema,
        charset='utf8',
        cursorclass=aiomysql.DictCursor,
        autocommit=True,
        minsize=config.db_pool_minsize,
        maxsize=config.db_pool_maxsize
    )
    return pool
