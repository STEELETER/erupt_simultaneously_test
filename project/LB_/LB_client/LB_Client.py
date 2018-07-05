import socket

from LB_.LB_Service.LB_Client.LB_Log import log
from LB_.LB_client.test_tomcat_ip import test_tomcat_ip


def User_client():
    """user_client"""

    global client_socket
    data_str = None
    dict_data = {'identity':'user','sysnum':'868608'}

    # while True:
    try:
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect(('172.21.1.13',6789))
        client_socket.send(str(dict_data).encode())
        #设置recv超时时间 2秒
        client_socket.settimeout(2)
        data_str = client_socket.recv(4096)
        #如果以接收到数据 将其解码返回
        if data_str:
            client_data_str = data_str.decode()
            log.info('----->已收到服务器真实ip：%s '% client_data_str)
            return client_data_str
        else:
        #如果没有收到数据 读取本地配置文件 返回配置文件信息
             return test_tomcat_ip(data_str)
    except Exception as e :
        #获取服务器返回ip失败 读取本地配置文件ip 有数据将其返回 无数据返回False

        log.info('《---------获取服务器真实ip失败 读取本地配置文件ip----------》')
        return test_tomcat_ip(data_str)

User_client()
# sysnum:868608






















