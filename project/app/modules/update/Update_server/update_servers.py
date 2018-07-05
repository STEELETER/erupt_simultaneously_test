import socket
import threading

from modules.update.Update_server.Update_server_log import logs
from modules.update.Update_server.get_conf_send import get_conf_send
from modules.update.Update_server.get_zip_send import get_zip_send


class UpdateServer():
    """版本升级 server"""
    def __init__(self):
        self.conf_path = 'C:/Users/zhongcun/Desktop/project/app/modules/update/Update_server/config.ini'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('172.21.1.13', 5656))
        self.s.listen(50)
        self.run()
    def update_server_version(self):
        """接收第一次请求"""
        # local_ip = socket.gethostbyname(socket.gethostname())

        global update_client, update_num, update_z
        while True:
            client_socket, address = self.s.accept()
            while True:
                try:
                    update_client = client_socket.recv(4096).decode()
                except Exception as e:
                    logs.error('》》》》server 接收数据出现异常： %s ' % e)

                if update_client:
                    logs.info('----->已接收到client请求 请求数据为：%s' % update_client)
                    if update_client == 'Revision':
                        # 读取配置文件版本号并发送
                       get_conf_send(self.conf_path,update_client,client_socket)

                    elif update_client == 'Filename':
                        #发送zip
                        get_zip_send(self.conf_path,update_client,client_socket)
                else:
                    break
    def run(self):

        logs.info('Update_server starting.....')
        self.update_server_version()


if __name__ == '__main__':
    t = threading.Thread(target=UpdateServer)
    t.start()


















