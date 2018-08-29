# -*- coding: utf-8 -*-
import aiomysql
from config import config
from .log import debug_log, info_log, warning_log, error_log


class Db:
    """Db sql execute using aiomysql pool."""
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
        """Executes the given select operation

        Executes the given select operation substituting any markers with
        the given parameters.

        For example, getting all rows where id is 5:
          Db.select("SELECT * FROM t1 WHERE id = %s", (5,))

        :param query: ``str`` sql statement
        :param args: ``tuple`` or ``list`` of arguments for sql query
        :param size: ``int`` or None, size rows returned
        :returns: ``list``
        """
        try:
            pool = await Db.get_db_pool()
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
                    if size is None:
                        result = await cursor.fetchall()
                    else:
                        result = await cursor.fetchmany(size)
                    rowcount = cursor.rowcount
        except Exception as e:
            if type(args) is list:
                args = tuple(args)
            error_log("db select errror [%s]: %s", query % args, e)
            raise
        return result, rowcount

    @staticmethod
    async def select_one(query, args):
        """Executes the given select operation, but only fetch one row.

        Executes the given select operation substituting any markers with
        the given parameters.

        For example, getting one row where id is 5:
          Db.select_one("SELECT * FROM t1 WHERE id = %s limit 1", (5,))

        :param query: ``str`` sql statement
        :param args: ``tuple`` or ``list`` of arguments for sql query
        :returns: ``dict``
        """
        try:
            pool = await Db.get_db_pool()
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
                    result = await cursor.fetchone()
                    rowcount = cursor.rowcount
        except Exception as e:
            if type(args) is list:
                args = tuple(args)
            error_log("db select one errror [%s]: %s", query % args, e)
            raise
        return result, rowcount

    @staticmethod
    async def insert(query, args):
        """Executes the given insert operation

        Executes the given insert operation substituting any markers with
        the given parameters.

        For example, insert table t1 one row:
          Db.insert("insert into t1(id, name) values (%s, %s)", (5, 'Jack'))

        :param query: ``str`` sql statement
        :param args: ``tuple`` or ``list`` of arguments for sql query
        :returns: ``int``, number of rows that has been produced of affected
        """
        pool = await Db.get_db_pool()
        async with pool.acquire() as conn:
            try:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
                    affected_rows = cursor.rowcount
                    lastrowid = cursor.lastrowid
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                if type(args) is list:
                    args = tuple(args)
                error_log("db insert errror [%s]: %s", query % args, e)
                raise
        return affected_rows, lastrowid

    @staticmethod
    async def insert_many(query, args):
        """Executes the given insert operation

        Executes the given insert operation substituting any markers with
        the given parameters.

        For example, insert table t1 many rows:
          Db.insert_many("insert into t1(id, name) values (%s, %s)", [(5, 'Jack'), (6,'Tom')])

        :param query: ``str`` sql statement
        :param args: ``tuple`` or ``list`` of arguments for sql query
        :returns: ``int``, number of rows that has been produced of affected
        """
        pool = await Db.get_db_pool()
        async with pool.acquire() as conn:
            try:
                async with conn.cursor() as cursor:
                    await cursor.executemany(query, args)
                    affected_rows = cursor.rowcount
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                error_log("db insert many errror [%s]: %s", query % list(args), e)
                raise
        return affected_rows

    @staticmethod
    async def update(query, args):
        """Executes the given update operation

        Executes the given update operation substituting any markers with
        the given parameters.

        For example, update table t1 where id is 5:
          Db.update("update t1 set name=%s where id=%s", ('Jack', 5))

        :param query: ``str`` sql statement
        :param args: ``tuple`` or ``list`` of arguments for sql query
        :returns: ``int``, number of rows that has been produced of affected
        """
        pool = await Db.get_db_pool()
        async with pool.acquire() as conn:
            try:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
                    affected_rows = cursor.rowcount
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                if type(args) is list:
                    args = tuple(args)
                error_log("db update errror [%s]: %s", query % args, e)
                raise
        return affected_rows
