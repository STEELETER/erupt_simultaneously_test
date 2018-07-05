import json

import requests
from PyQt5.QtCore import QThread, pyqtSignal

from common import db
from common import context
from modules.update.Update_clients.Update_clients import UpdateClient


#获取lb地址





def get_lb_addr():
    server_ip = ''
    server_port = ''
    ca_ip = ''

    result = db.find('select * from sys_param ','')

    if len(result) > 0:
        server_ip = result[0]['server_ip']
        server_port = result[0]['server_port']
        ca_ip = result[0]['ca_ip']
    print([server_ip,server_port,ca_ip])
    return [server_ip,server_port,ca_ip]


class Entry(QThread):

    abort = pyqtSignal(str)
    def __init__(self,uname="",pwd="",pin=""):
        super(Entry,self).__init__()

        self.result = False
        self.result_info = ""

        lb_address = get_lb_addr()
        self.lb_addr = (lb_address[0],lb_address[1])
        self.tomcat_addr = ("","")
        self.data = {
            "uname":uname,
            "pwd":pwd,
            "pin":pin
        }


    #连接lb服务
    def connect_lb(self):
        print("连接lb服务")

        self.tomcat_addr = self.lb_addr
        self.base_tomcat_url =  "http://%s:%s/snspro/"%(str(self.tomcat_addr[0]),str(self.tomcat_addr[1]))
        context.set("tomcat_addr",(self.tomcat_addr[0],self.tomcat_addr[1]))

    def update_client(self):
        """更新客户端"""
        UpdateClient()

    def get_random_num(self):
        # result = False
        # try:
            url = self.base_tomcat_url+"userController.do?returnNum"
            print(url)
            response = requests.get(url)
            result=response.content.decode()
            result = json.loads(result)
            self.data['random1'] = str(result['strNum1'])
            self.data['random2'] = str(result['strNum2'])
            print("获取到的随机数是：%s"%str(result))
        #     result = True
        # except Exception as e:
        #     print(e)
        #
        # return result

    def check_user_info(self):
        try:
            arg_encode = {"a":self.data['uname'],"b":self.data['pwd'],"c":self.data['random1']}
            check_url = self.base_tomcat_url+"userController.do?linuxfirstother"

            response  = requests.post(url=check_url, data=arg_encode)
            check_result = response.content.decode()

            check_result = json.loads(check_result)

            self.result = check_result['flag']
            self.result_info = check_result['errMgr']

        except Exception as e:
            print(e)
            self.result = False
            self.result_info ="服务器连接失败"
        finally:


            if not self.result:
                # self.result = False
                # self.result_info = result['errMgr']
                # print(self.result_info)

                # self.terminate()
                # self.abort.connect(raise_error)
                self.abort.emit(self.result_info)

            else:
                self.result = True


        # print("获取到的随机数是：%s"%str(result))

    def login_success(self):
        print("登录成功")
        context.set("login_data",self.data)

    def boot_snspro_home(self):
        arg_encode = {"a":self.data['uname'],"b":self.data['pwd'],"c":self.data['random2']}
        set_url = self.base_tomcat_url+"userController.do?linuxmainother"

        response  = requests.post(url=set_url, data=arg_encode)
        result = response.content.decode()
        print(result)
        context.set("snspro_home",result)

    #主逻辑
    def run(self):
        try:
            self.connect_lb()
            self.update_client()
            self.get_random_num()
            self.check_user_info()
            # print(result)
            if self.result:
                self.login_success()
        except Exception as e:
            print("服务器连接失败")
        # while True:
        #     print(1)

# def raise_error(msg):
#      login = context.get('login')
#      print(login)
#      login.raise_error(msg)