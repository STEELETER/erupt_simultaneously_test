
import socket

from modules.update.Update_clients.get_config import get_config
from modules.update.Update_clients.update_client_log import logc
from modules.update.Update_clients.update_client_zip import update_client_zip


class UpdateClient():
    """版本升级client端"""

    def __init__(self):
        self.update='Filename'
        self.versions = 'Revision'
        self.conf_path = 'C:/Users/zhongcun/Desktop/project/app/modules/update/Update_clients/Config2.ini'
        self.update_scoket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.update_scoket.connect(('172.21.1.13',5656))
        self.run()

    def run(self):
        self.update_client()


    def update_client(self):
        """客户端第一次请求版本号"""

        global server_data
        # 获取client的版本号
        versions_client = get_config(self.conf_path)
        logc.info('----->已经获取到client的当前版本为：%s' % versions_client)
        #  接收版本号
        try:
            self.update_scoket.send(self.versions.encode())
            logc.info('----->client端第一次发送获取版本号请求已发送 发送数据为：%s' % self.versions)
        except Exception as e :
            logc.error('》》》》client端发送获取版本号请求出现异常：%s ' % e)
        try:
            server_data = self.update_scoket.recv(10240).decode()
            logc.info('----->已接收到server响应的版本号为：%s' % server_data)
        except Exception as e :
            logc.error('》》》》client端 接收数据出现异常：%s' % e)
        #  将获取的版本号 跟自己进行对比
        if server_data == versions_client:
            logc.info('-----》温馨提示：您已经是最新版本啦 无需更新 即将关闭套接字')
            self.update_scoket.close()
        else:
            # 向服务器发送zip请求
            update_client_zip(self.update_scoket, self.update)

if __name__ == '__main__':

   UpdateClient()














