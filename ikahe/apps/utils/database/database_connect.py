import pymysql, pymssql
from DBUtils.PooledDB import PooledDB
from utils.database.settings import MYSQL, MSSQL_erp, MSSQL_mes


# import sentry_sdk
#
# # sentry报错收集服务器
# sentry_sdk.init("https://89f2e30912c64c1c8b4da5b739e706a8@sentry.io/1876964")


# 装饰器用于使用with开关调用__enter__ 和 __exit__
def db_conn(func):
    def wrapper(self, *args, **kw):
        with self as db:
            result = func(self, db, *args, **kw)
        return result

    return wrapper


# mssql 结果转换dict
def get_dict(row_list, col_list):
    cols = [d[0] for d in col_list]
    res_list = []
    for row in row_list:
        res_list.append(dict(zip(cols, row)))  # 将两个列表合并成一个字典 dict(zip())方法
    return res_list


class DatabasePool(object):
    def __init__(self, db):
        self.type = db
        if self.type == "mysql":
            config = {
                'creator': pymysql,
                'host': MYSQL['HOST'],
                'port': MYSQL['PORT'],
                'user': MYSQL['USER'],
                'passwd': MYSQL['PASSWD'],
                'db': MYSQL['DB'],
                'charset': MYSQL['CHARSET'],
                'maxconnections': 20,  # 连接池最大连接数量
                'cursorclass': pymysql.cursors.DictCursor
            }
        elif self.type == 'core_erp':
            config = {
                'creator': pymssql,
                'host': MSSQL_erp['HOST'],
                # 'port': MSSQL['PORT'],
                'user': MSSQL_erp['USER'],
                'password': MSSQL_erp['PASSWD'],
                'database': MSSQL_erp['DB'],
                'charset': MSSQL_erp['CHARSET'],
                'maxconnections': 20,  # 连接池最大连接数量
                # 'cursorclass': pymysql.cursors.DictCursor
            }
        elif self.type == 'core_win':
            config = {
                'creator': pymssql,
                'host': MSSQL_mes['HOST'],
                # 'port': MSSQL['PORT'],
                'user': MSSQL_mes['USER'],
                'password': MSSQL_mes['PASSWD'],
                'database': MSSQL_mes['DB'],
                'charset': MSSQL_mes['CHARSET'],
                'maxconnections': 20,  # 连接池最大连接数量
                # 'cursorclass': pymysql.cursors.DictCursor
            }
        self.pool = PooledDB(**config)

    def __enter__(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()

    # 查询sql
    @db_conn
    def ExecQuery(self, db, sql, p, *args, **kw):
        db.cursor.execute(sql, p)
        relist = db.cursor.fetchall()
        return relist
        # if self.type == 'mysql':
        #     return relist
        # else:
        #     desc_res = db.cursor.description
        #     return get_dict(relist, desc_res)

    # 非查询的sql
    @db_conn
    def ExecNoQuery(self, db, sql, p, *args, **kw):
        try:
            db.cursor.execute(sql, p)
            db.conn.commit()
            print("执行成功！")
        except Exception as e:
            db.conn.rollback()
            print(e)

    @db_conn
    def ExecProc(self, db, proc, p, *args, **kwargs):
        try:
            db.cursor.callproc(proc, p)
            relist = db.cursor.nextset()
            db.conn.commit()
            print(relist)
            print("执行成功！")
            return relist
        except Exception as e:
            db.conn.rollback()
            print(e)


class Parameters(dict):
    def __init__(self):
        super().__init__()

    def add(self, key, value):
        super().__setitem__(
            key, value)
        return self


class Par(list):
    def __init__(self):
        super().__init__()

    def add(self, p):
        self.append(p)
        return self


if __name__ == '__main__':
    # connect = DatabasePool('mysql')
    #
    # lists = connect.ExecQuery('select * from goods_goods limit 3')
    #
    # for i in lists:
    #     print(i)
    #
    # connect.ExecNoQuery("update goods_goods set goods_sn='6666'  where id=52")

    #########
    ##mssql##
    #########
    sql = 'select * from fm_work_line where code = %s'

    p = Parameters()
    p.add('work_line', 'Line2（包装）').add('code', 'Line2（包装）')
    print(p['code'])

    p = ('YH001',)
    #
    connect = DatabasePool('core_win')
    lists = connect.ExecQuery(sql, p)

    # print(lists)
    #
    for i in lists:
        print(i)

    # connect.ExecNoQuery('update mm_item set category_id=12  where id = 1')

    # connect =DatabasePool('core_erp')
    #
    # proc = 'p_mm_wo_workshop_plan_get_items_finereport'
    # p = ()
    # list = connect.ExecProc(proc,p)
    #
    # print(list)
