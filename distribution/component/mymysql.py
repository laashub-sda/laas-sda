from contextlib import closing

import pymysql
from DBUtils.PooledDB import PooledDB

from . import mymysql
from ..exception import MyServiceException

db_pool = None
"""
https://cito.github.io/DBUtils/UsersGuide.html#pooleddb
"""


def init(mysql_config):
    if not db_pool:
        mysql_config["cursorclass"] = pymysql.cursors.DictCursor
        mymysql.db_pool = PooledDB(pymysql, **mysql_config)


def execute(sql, parameters={}):
    try:
        with closing(mymysql.db_pool.connection()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, parameters)
                # consider it INSERT or other
                if sql.strip()[:len("INSERT")].upper() == "INSERT":
                    execute_result = cursor.lastrowid
                else:
                    execute_result = cursor.fetchall()
                if sql.strip()[:len("SELECT")].upper() != "SELECT":
                    conn.commit()
    except Exception as e:
        raise MyServiceException("execute sql error: " + str(e))
    return execute_result
