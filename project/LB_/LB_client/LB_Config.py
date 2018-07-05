import configparser
import random

from LB_.LB_Service.LB_Client.LB_Log import log

"""通过 配置文件路径 r 文件 将随机的真实ip返回"""
conf_path = 'C:/Users/zhongcun/PycharmProjects/untitled/LB_client/Config.ini'
# conf_path = 'config.ini'
real_ip_list = []

#获取随机服务器ip
def get_random_ip():

    return real_ip_list
try:
    #配置文件
    cf = configparser.ConfigParser()
    cf.read(conf_path)  # 文件路径
    b=random.randint(1,5)
    real_ips_str = cf.get("server_ips",'ips')  # 获取指定section 的option值
    real_ip_list = real_ips_str.split(',')
    # print(real_ip_list)

except Exception as e:
    log.info('【lb-warn】读取配置文件时出错！[%s]'%str(e))
    # print(e)

get_random_ip()


