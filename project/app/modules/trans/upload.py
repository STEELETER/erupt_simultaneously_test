import json
import os
import queue
import socket

import sys

import threading
import time

import binascii
import uuid
from PyQt5 import QtCore

import pysm4.sm4
from PyQt5.QtCore import pyqtSignal, QThread, QObject

# from modules.notice.controller import add
from modules.trans.trans_pool import pool, add_to_pool, test
from common.check import check_sysnum
from common.conf import trans_per_size, updown_serv_addr
from common.fileTool import getFileMd5
from common.sock import Soc_client, socket_recv_dict, socket_send_json
from common import db
# from modules.notice import controller as notice


'''
Uploader('{"id":"xxxx","up_from":"xxxxxxxx","up_to":"xxxxxxx"}')

'''

class Uploader(QThread):
     # 定义一个信号
     # finished = pyqtSignal(str)
     def __init__(self,up_json,addr=updown_serv_addr):
         try:
             super(Uploader, self).__init__() #注意：一定要显式的调用父类的初始化函数。
             # print("--------2------------")

             self.result = False
             self.result_info = "上传失败"
             self.has_send_percent = 0

             self.__addr = addr
             self.__up_json = up_json

             self.__thread_mgr()
             self.__mk_sock_client()
             self.start()
         except Exception as e:
             print('异常%s'%str(e))

    #线程管理，方便实现挂起和恢复
     def __thread_mgr(self):
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

     #创建客户端socket
     def __mk_sock_client(self):
         client_socket = Soc_client(self.__addr)
         self.__client = client_socket.socket

     #向服务器验证该文件信息
     def __check_file(self):
         #发送
         checkInfo = {'order':'add','fpath':self.up_to['fpath'],'fsize':self.up_from['fsize']}
         print("发送到服务器的文件验证信息：%s"%str(checkInfo))
         socket_send_json(self.__client,checkInfo)

         #接收
         result = socket_recv_dict(self.__client)
         print('接收到服务器的返回信息：%s'%str(result))

         self.has_send = 0
         self.__finish = False
         try:
            self.has_send = int(result['has'])
            self.__finish = bool(result['finish'])
         except Exception as e:
            print('服务器发送的文件已发送量格式错误！')
            raise

     def __create_result(self,isok=False,info=""):
         self.result = isok
         if isok:
            self.result_info = "上传成功！"
         else:
            self.result_info = "上传失败：%s"%str(info)

     def __send_file(self):
         with open(self.up_from['fpath'], 'rb') as f:
            self.turn_db_state(1)
            f.seek(self.has_send)  # 定位到已经传到的位置
            while self.has_send < int(self.up_from['fsize']) and self.__running.isSet():
                self.__flag.wait()
                data = f.read(trans_per_size)

                #每次发包之前的操作
                data = self.per_before_send(data)

                #更新到__has_send属性
                self.__client.send(data)
                self.has_send += len(data)

                #每次发包之后的操作
                self.per_after_send()

         result = socket_recv_dict(self.__client)  # 确认是否已上传成功
         print('\n确认文件是否上传成功信息：%s'%str(result))

         finish = bool(result['finish'])
         if finish:
             self.__create_result(True)
             # notice.add(self.fname)
             # self.finished.connect(test)
             self.finished.emit(self.fname)
             # notice.add(self.fname)
         else:
             self.__create_result(info="上传后的文件大小与原文件不一致！")

    #每次发包之前的操作
     def per_before_send(self,data):
         #加密pysm4
        # print(type(data))
        # data = pysm4.sm4.encrypt_ecb(str(data),'123456')


        # data = data.encode("utf-8")
        # print(type(data))

        return data

     #每次发包之后的操作
     def per_after_send(self):
         # pass
        # 动态打印上传进度
        self.has_send_percent = int(self.has_send /self.up_from['fsize'] * 100)
        sys.stdout.write('\r')  # 清空文件内容
        sys.stdout.write('已发送%s%%|%s' % (self.has_send_percent, (round(self.has_send /self.up_from['fsize'] * 40) * '★')))
        sys.stdout.flush()  # 强制刷出内存

        # db.update_dict("upload",{"has_send":self.has_send},"fileId='%s'"%self.fileId)


     #格式化请求信息
     def __make_dict(self):
         up_dict = json.loads(self.__up_json)

         fpath = up_dict['up_from']
         fsize = os.path.getsize(fpath)

         self.fileId = up_dict['id']
         self.fname = os.path.basename(fpath)
         self.up_from = object
         self.up_from = {
             'fpath':fpath,
             'fsize':fsize
         }
         self.up_to = {
             'fpath':up_dict['up_to']
         }

         #添加入线程池
         add_to_pool(self.fileId,self)

     #存储数据库
     def store_db(self):
         print("-----------------------------------")
         # hash = getFileMd5(self.up_from['fpath'])
         # # has_file = db.has("upload","file_hash='%s'"%hash)
         # # print(has)
         db.insert_dict("upload",{
             "id":str(uuid.uuid1()),
             "fname":os.path.basename(self.up_from['fpath']),
             "fileId":self.fileId,
             "local_path":self.up_from['fpath'],
             "server_path":self.up_to['fpath'],
             "fsize":int(self.up_from['fsize']),
             "has_send":0,
             "up_state":0,
             'file_hash':"",
             'create_time':int(time.time()),
             'update_time':int(time.time())
         })
        # pass

     #改变数据库记录的上传状态
     def turn_db_state(self,state_num):
         pass
         # db.update_dict("upload",{"up_state":state_num},"fileId='%s'"%self.fileId)

     def run(self):
        try:
            #1.格式化请求信息
            self.__make_dict()

            #存储数据库
            self.store_db()

             #2.验证文件信息
            self.__check_file()

            #3.a.服务器无该文件 b.服务器文件有temp
            if self.__finish:
                self.__create_result(True)
            else:
                #发送文件
                self.__send_file()

        except Exception as e:
             self.__create_result(info= str(e))
        finally:
             #4.最后操作
            self.after_all()

     #最后操作
     def after_all(self):
       try:
            self.__client.close()
            print("\n%s"%str(self.result_info))
       except Exception as e:
            print(e)

     #暂停上传
     def suspend(self):
         try:
            # self.__client.close()
            self.__flag.clear()     # 设置为False, 让线程阻塞
            self.turn_db_state(2)
         except:
             print("关闭当前连接")
     def resume(self):
        try:
             # self.__mk_sock_client()
             # self.run()
             self.__flag.set()    # 设置为True, 让线程停止阻塞
             self.turn_db_state(1)
        except Exception as e:
            print("恢复连接")

    #删除服务器上的文件
     def __remove_serv_file(self):
         socket_send_json(self.__client,{'order':'del','fpath':self.up_to['fpath']})

    #取消上传
     def cancel(self):
         try:
             self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
             self.__running.clear()        # 设置为False
             self.__remove_serv_file()
         except:
            print("取消上传失败")
         finally:
             self.__client.close()


def start():
    print('上传下载开始了...')
    # while True:
    #     pass

# if __name__=="__main__":
    # dict = {}
    # dict['sysnum'] = '868608'
    # dict['source'] = {'fpath':'xxxx','fsize':'xxxx'}
    # print(os.path.getsize('C:/Users/Administrator/Desktop/new_app/src/web/web1.zip'))

    # add_list_up('{"sysnum":"868608","up_list":[{"id":"1","up_from":"F:/eclipse-jee-kepler-SR2-win32.zip","up_to":"D:/eclipse-jee-kepler-SR2-win32.zip"},{"id":"2","up_from":"F:/cn_visio_professional_2016_x86_x64_dvd.rar","up_to":"D:/cn_visio_professional_2016_x86_x64_dvd.rar.zip"},{"id":"3","up_from":"F:/Adobe Photoshop CS6  roustar31中文特别版.exe","up_to":"D:/Adobe Photoshop CS6  roustar31中文特别版.exe"}]}')

    # pool.submit(Uploader,('{"sysnum":"868608","up_from":"F:/eclipse-jee-kepler-SR2-win32.zip","up_to":"D:/eclipse-jee-kepler-SR2-win32.zip"}'))
    # pool.submit(Uploader,('{"sysnum":"868608","up_from":"F:/Adobe Photoshop CS6  roustar31中文特别版.exe","up_to":"D:/Adobe Photoshop CS6  roustar31中文特别版.exe"}'))
    # pool.submit(Uploader,('{"sysnum":"868608","up_from":"F:/xmind-8-windows-wm.exe"},"up_to":"D:/xmind-8-windows-wm.exe"}}'))

    # up = Uploader('{"sysnum":"868608","up_from":{"fpath":"F:/eclipse-jee-kepler-SR2-win32.zip"},"up_to":{"fpath":"D:/eclipse-jee-kepler-SR2-win32.zip"}}')
    # print (sqlite3.sqlite_version)
    # values = [  '\"{}\"'.format(item) for item in ["4e9f13795ec595ba688c087cb9f5c6eb", 0, 262513701, 0, 1526528707, 1526528707, 'F:/eclipse-jee-kepler-SR2-win32.zip', 'D:/eclipse-jee-kepler-SR2-win32.zip', 'eclipse-jee-kepler-SR2-win32.zip', 'b0791ad2-5984-11e8-aae7-005056c00008']]
    # print(",".join(values))

    # data = pysm4.encrypt(pysm4.sm4._hex('佛挡杀佛').decode(),00000)
    # t = int(time.time())
    # array = time.localtime(t)
    # otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", array)
    # print(otherStyleTime)

    # print(uuid.uuid1())
    # up1 = Uploader('{"sysnum":"868608","up_from":{"fileId":"85236974150000","fpath":"F:/eclipse-jee-kepler-SR2-win32.zip"},"up_to":{"fpath":"D:/eclipse-jee-kepler-SR2-win32.zip"}}')
    # up2 = Uploader('{"sysnum":"868608","up_from":{"fileId":"85236974150000","fpath":"F:/xmind-8-windows-wm.exe"},"up_to":{"fpath":"D:/xmind-8-windows-wm.exe"}}')
    # up3 = Uploader('{"sysnum":"868608","up_from":{"fileId":"85236974150000","fpath":"F:/Java资料1（内部）.rar"},"up_to":{"fpath":"D:/Java资料1（内部）.rar"}}')
    # up4 = Uploader('{"sysnum":"868608","up_from":{"fileId":"85236974150000","fpath":"F:/AdobePhotoshopCS6.rar"},"up_to":{"fpath":"D:/AdobePhotoshopCS6.rar"}}')
    # time.sleep(3)
    # up.cancel()
    # up.suspend()
    # up1.suspend()
    # time.sleep(10)
    # up.resume()
    # up1.resume()

    # F = open("D:/8523697415",'r')
    # F.truncate(10240)
    # print(os.path.splitext('D:/新建文件夹/8523697415.exe.tmp'))

    # os.rename('D:/8523697415', 'D:/8523697415.tmp')
    # print( "%s.tmp"%str("D:/8523697415"))

    # while True:
    #     sock = Soc_client(('172.21.1.200',7100))
    #     sock.socket.send('fsdfsdfasdfasdfasdfasaaaaaaaaaaaaaaaa'.encode())
    #     print("-----")
