# coding:utf-8
# 处理mysql数据操作的

import pymysql
import sys
import logging
from mysql import config

# 获取logging实例
logger = logging.getLogger("baseSpider")
# 日志输出格式
formatter = logging.Formatter('%(asctime)s%(levelname)-8s:%(message)s')
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)


class MysqlDb:
    conn = None
    cursor = None
    result = None
    def __init__(self):
        # 建立数据库连接
        self.conn = pymysql.connect(
            host = config.mysql_config['host'],
            user = config.mysql_config['user'],
            password = config.mysql_config['password'],
            port = config.mysql_config['port'],
            database = config.mysql_config['database'],
        )
        self.cursor = self.conn.cursor()

    # 查询一条数据
    def selectOne(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            logger.info("查询成功")
            return result
        except Exception as e:
            logger.error(e)

    # 查询多条数据
    def selectMany(self, sql, num):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchmany(num)
            logger.info("查询成功")
            return result
        except Exception as e:
            logger.error(e)

    # 查询所有数据
    def selectAll(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            logger.info("查询成功")
            return result
        except Exception as e:
            logger.error(e)

    #对数据库进行增删改
    def execute_sql(self,sql,data=None):
        try:
            if data is None:
                self.cursor.execute(sql)
                self.conn.commit()
                logger.info("操作成功")
                return "执行操作成功"
            else:
                self.cursor.executemany(sql,data)
                self.conn.commit()
                logger.info("操作成功")
                return "执行操作成功"
        except Exception as e:
            print(e)
            self.conn.rollback()

    #对象资源被释放时触发，在对象即将被删除时的最后操作
    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()
