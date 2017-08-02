# -*- coding: utf-8 -*-
import aiomysql
from config import config
from .log import debug_log, info_log, warning_log, error_log


class Db:
    __db_pool = {'mysql': None}

    @staticmethod
    async def create_db_pool(loop=None):
        if Db.__db_pool['mysql'] is not None:
            return Db.__db_pool['mysql']

        Db.__db_pool['mysql'] = await aiomysql.create_pool(
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

        return Db.__db_pool['mysql']

    @staticmethod
    async def get_db_pool():
        if Db.__db_pool['mysql'] is None:
            return await Db.create_db_pool()
        else:
            return Db.__db_pool['mysql']

    @staticmethod
    async def select(query, args, size=None):
        result = None
        try:
            pool = await Db.get_db_pool()
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
                    if size is None:
                        result = await cursor.fetchall()
                    else:
                        result = await cursor.fetchmany(size)
        except Exception as e:
            error_log("db select errror [%s]: %s", query % tuple(args), e)
        return result

    @staticmethod
    async def select_one(query, args):
        result = None
        try:
            pool = await Db.get_db_pool()
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
                    result = await cursor.fetchone()
        except Exception as e:
            error_log("db select one errror [%s]: %s", query % tuple(args), e)
        return result

    @staticmethod
    async def insert(query, args):
        affected_rows = 0
        pool = await Db.get_db_pool()
        async with pool.acquire() as conn:
            try:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
                    affected_rows = cursor.rowcount
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                affected_rows = 0
                error_log("db insert errror [%s]: %s", query % tuple(args), e)
        return affected_rows

    @staticmethod
    async def insert_many(query, args):
        affected_rows = 0
        pool = await Db.get_db_pool()
        async with pool.acquire() as conn:
            try:
                async with conn.cursor() as cursor:
                    await cursor.executemany(query, args)
                    affected_rows = cursor.rowcount
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                affected_rows = 0
                error_log("db insert many errror [%s]: %s", query % tuple(args), e)
        return affected_rows

    @staticmethod
    async def update(query, args):
        affected_rows = 0
        pool = await Db.get_db_pool()
        async with pool.acquire() as conn:
            try:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
                    affected_rows = cursor.rowcount
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                affected_rows = 0
                error_log("db update errror [%s]: %s", query % tuple(args), e)
        return affected_rows
