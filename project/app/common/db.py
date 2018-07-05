# python sqlite
import os
import sqlite3

from common import conf


Conn = None
Cursor = None

def open_db():
    '''获取到数据库的连接对象，参数为数据库文件的绝对路径
    如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
    路径下的数据库文件的连接对象；否则，返回内存中的数据接
    连接对象'''
    global Conn,Cursor
    # path = conf.db_path
    path = 'C:/Users/zhongcun/Desktop/project/app/resource/data/db/data.db'
    print("数据库地址："+path)
    Conn = sqlite3.connect(path,check_same_thread = False)
    Conn.row_factory = sqlite3.Row
    if os.path.exists(path) and os.path.isfile(path):
        Cursor = Conn.cursor()
    else:
        Cursor = None

###############################################################
####            创建|删除表操作     END
###############################################################

def close_db():
    '''关闭数据库游标对象和数据库连接对象'''
    if Cursor is not None:
        Conn.commit()
        Cursor.close()
        Conn.close()



###############################################################
####            数据库操作CRUD     START
###############################################################

def insert(tb,keys,values):
    print(keys)
    print(values)
    '''插入数据'''
    result = False
    try:
        print('开始')
        if tb != '' and len(keys)>0 and len(values)>0:
            if len(keys)== len(values):
                values = ['\"{}\"'.format(item) if isinstance(item,str) else str(item) for item in values ]
                sql = 'insert into {}({}) values ({})'.format(tb, ",".join(keys), ",".join(values))
                print('执行sql:{}'.format(sql))
                print('-----2')
                Cursor.execute(sql)
                result = True
    except Exception as e:
        print(str(e))
    return result




def find(sql, data):
    '''查询一条数据'''
    if sql is not None and sql != '':
        if data is not None:
            # Do this instead
            d = (data,) if data !='' else ''
            print('执行sql:[{}],参数:[{}]'.format(sql, data))
            Cursor = Conn.cursor()
            Cursor.execute(sql,d)
            records = Cursor.fetchall()
            return records
        else:
            print('the [{}] equal None!'.format(data))
            return []
    else:
        print('the [{}] is empty or equal None!'.format(sql))


def update(tb,sets_str,where):
    result = False
    try:
        '''更新数据'''
        if tb != '' and sets_str!='' and where!='':
            sql = 'update {} set {} where {}'.format(tb,sets_str,where)
            print('执行sql:{}'.format(sql))
            Cursor.execute(sql)
            result = True
    except Exception as e:
        print(str(e))
    finally:
        pass
    return result



def has(tb,where='1=1'):
    sql = 'select * from %s where %s'%(str(tb),str(where))
    list = find(sql,'')
    return len(list) > 0

def insert_dict(tb,dict_data):
    result = False
    if isinstance(dict_data,dict):
        keys = []
        values = []
        for k,v in dict_data.items():
            keys.append(k)
            values.append(v)
        result = insert(tb,keys,values)
    return result

def update_dict(tb,dict_data,where='1=1'):
    result = False
    if isinstance(dict_data,dict):
        sets = []
        for k,v in dict_data.items():
            v_str = '\"{}\"'.format(v) if isinstance(v,str) else str(v)
            sets.append('{}={}'.format(k,v_str))
        result = update(tb,",".join(sets),where)
    return result





