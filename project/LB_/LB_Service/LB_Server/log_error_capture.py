
from LB_Service.LB_Server import LB_Log


# def logger(func):
#     def inner(*args, **kwargs):
#         # fliename_log = 'C:/Users/zhongcun/Desktop/project/app/common/conf.py'
#         global log
#         try:
#             log = LB_Log.Logger(fliename_log)
#             func(*args, **kwargs)
#             # log.info(result)
#         except Exception as e:
#             log.error('异常错误为：%s'%e)
#     return inner
#
#
# @logger
# def test():
#     print(2 / 0)
# test()
#
# # test2(10)
# print()