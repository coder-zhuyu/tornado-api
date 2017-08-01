# -*- coding: utf-8 -*-
import aiomysql
from config import config

__db_pool = {'mysql': None}


async def create_db_pool(loop=None):
    if __db_pool['mysql'] is not None:
        return __db_pool['mysql']

    __db_pool['mysql'] = await aiomysql.create_pool(
        host=config.db_host,
        port=config.db_port,
        user=config.db_user,
        password=config.db_password,
        db=config.db_schema,
        charset='utf8',
        cursorclass=aiomysql.DictCursor,
        autocommit=True,
        minsize=config.db_pool_minsize,
        maxsize=config.db_pool_maxsize,
        connect_timeout=config.db_connect_timeout,
        loop=loop
    )

    return __db_pool['mysql']


async def get_db_pool():
    if __db_pool['mysql'] is None:
        return await create_db_pool()
    else:
        return __db_pool['mysql']
