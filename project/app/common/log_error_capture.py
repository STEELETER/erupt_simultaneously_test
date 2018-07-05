
"""
在conf.py 中配置文件名字为  fliename_log = 'flie_log.log'

"""

from common import log,conf
def logger(func):
    def inner(*args, **kwargs):
        flie_log = conf.fliename_log
        global logs
        try:
            logs = log.Logger(flie_log)
            func(*args, **kwargs)
        except Exception as e:
            logs.error('----->异常错误为：%s' % e)
    return inner




