import json
import os
import socket

import sys

import threading
import time

from modules.trans.trans_pool import add_to_pool
from common.check import check_sysnum
from common.conf import trans_per_size, updown_serv_addr
from common.sock import Soc_client, socket_recv_dict, socket_send_json

'''
'{"id":"xxxxx","down_from":"xxxx","down_to":"xxxxxxx"}'

'''


class Downloader():
     def __init__(self,down_json,addr=updown_serv_addr):
         try:
             super(Downloader, self).__init__() #注意：一定要显式的调用父类的初始化函数。

             self.result = False
             self.result_info = ""

             self.__addr = addr
             self.__down_json = down_json

             self.__thread_mgr()
             self.__mk_sock_client()
             self.run()
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
         checkInfo = {'order':'down','fpath':self.down_from['fpath'],'has_down':self.down_to['has_down']}
         print("发送到服务器的文件验证信息：%s"%str(checkInfo))
         socket_send_json(self.__client,checkInfo)

         #接收
         result = socket_recv_dict(self.__client)
         print('接收到的服务器返回验证返回信息：%s'%str(result))

         self.__fsize = 0
         self.__exist = False
         try:
            self.__exist = bool(result['exist'])
            self.__fsize = int(result['fsize'])
         except Exception as e:
            print('服务器发送的文件已发送量格式错误！')

     def __down_file(self):
         with open(self.down_to['temp_path'], 'wb') as f:
            f.seek(self.__has_down)  # 定位到已经传到的位置
            while self.__has_down < int(self.__fsize) and self.__running.isSet():
                self.__flag.wait()
                data = self.__client.recv(trans_per_size)

                #每次接收包之前的动作
                data = self.per_before_down(data)

                #写入文件
                f.write(data)
                self.__has_down += len(data)

                #每次下载后的相关操作
                self.per_after_down()

         has_recv = os.path.getsize(self.down_to['temp_path']) # 计算文件大小
         if int(has_recv)==int(self.__fsize):
            os.rename(self.down_to['temp_path'],self.down_to['fpath'])
            self.__create_result(True)
            # log.info("[trans-info]服务器已生成[%s]文件,大小为%s，与原文件大小一致"%(str(fpath),str(fsize)))
            # return_info(has=has_recv,finish="True")
         else:
            self.__create_result(info="下载后的文件与原文件大小不一致！！！")

            # log.info("【trans-warn】服务器已生成[%s]文件,大小为%s,与原文件大小不一致！%s"%(str(fpath),str(fsize)))

     def __create_result(self,isok=False,info=""):
         self.result = isok
         if isok:
            self.result_info = "下载成功！"
         else:
            self.result_info = "下载失败：%s"%str(info)

      #每次下载之前的动作
     def per_before_down(self,data):
         return data


     #下载过程中的相关操作
     def per_after_down(self):
        pass
        #动态打印下载进度
        # sys.stdout.write('\r')  # 清空文件内容
        # sys.stdout.write('已下载%s%%|%s' % (int(self.__has_down /self.__fsize * 100), (round(self.__has_down /self.__fsize * 40) * '★')))
        # sys.stdout.flush()  # 强制刷出内存

     #格式化请求信息
     def __make_dict(self):
         down_dict = json.loads(self.__down_json)

         fpath = down_dict['down_to']
         has_down = 0
         tmp_path = "%s.tmp"%str(fpath)
         if os.path.exists(fpath):
             self.__create_result(info="本地有同名文件！！！")
             raise Exception("本地有同名文件")
         elif os.path.exists(tmp_path):
            has_down = os.path.getsize(tmp_path)

         self.fileId = down_dict['id']
         self.down_from = {
             'fpath':down_dict['down_from'],
         }
         self.down_to = {
             'fpath':fpath,
             'has_down':str(has_down),
             'temp_path':tmp_path
         }
         self.__has_down = has_down

         #添加入线程池
         add_to_pool(self.fileId,self)

    #主函数
     def run(self):
        try:
            #1.格式化请求信息
            self.__make_dict()

             #2.验证文件信息
            self.__check_file()

            #3.服务器有该文件且大小不为0
            if self.__exist and self.__fsize!=0:
                #下载文件
                self.__down_file()
            else:
                self.__create_result(info= "服务器无该文件！！！")

        except Exception as e:
            self.__create_result(info= str(e))
        finally:
             #4.最后操作
            self.after_all()


      #4.最后操作
     def after_all(self):
        try:
            self.__client.close()
            print("\n%s"%str(self.result_info))
            if not self.result and hasattr(self,'down_to'):
                if self.down_to['temp_path']:
                    os.remove(self.down_to['temp_path'])
        except Exception as e:
            print(e)

     #暂停下载
     def suspend(self):
         try:
            # self.__client.close()
            self.__flag.clear()     # 设置为False, 让线程阻塞
         except:
             print("关闭当前连接")

     #恢复下载
     def resume(self):
        try:
             # self.__mk_sock_client()
             # self.run()
             self.__flag.set()    # 设置为True, 让线程停止阻塞
        except Exception as e:
            print("恢复连接")

    #删除本地临时文件
     def __remove_local_file(self):
        if os.path.exists(self.down_to['temp_path']):
            os.remove(self.down_to['temp_path'])

    #取消下载
     def cancel(self):
         try:
             # self.__client.close()
             self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
             self.__running.clear()        # 设置为False
             self.__remove_local_file()
         except:
            print("取消下载失败")
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

    # down = Downloader('{"sysnum":"868608","down_from":{"fpath":"F:/eclipse-jee-kepler-SR2-win32.zip"},"down_to":{"fileId":"8523697415","fpath":"D:/eclipse-jee-kepler-SR2-win32.zip"}}')
    # down1 = Downloader('{"sysnum":"868608","down_from":{"fpath":"F:/cn_visio_professional_2016_x86_x64_dvd.rar"},"down_to":{"fileId":"8523697415","fpath":"D:/cn_visio_professional_2016_x86_x64_dvd.rar"}}')
    # os.rename("D:/eclipse-jee-kepler-SR2-win32.zip.tmp","D:/eclipse-jee-kepler-SR2-win32.zip")
    # print(os.path.getsize('F:/developer.mozilla.org.tar.gz'))

    # up1 = Uploader('{"sysnum":"868608","up_from":{"fileId":"85236974150000","fpath":"F:/eclipse-jee-kepler-SR2-win32.zip"},"up_to":{"fpath":"D:/eclipse-jee-kepler-SR2-win32.zip"}}')
    # up2 = Uploader('{"sysnum":"868608","up_from":{"fileId":"85236974150000","fpath":"F:/xmind-8-windows-wm.exe"},"up_to":{"fpath":"D:/xmind-8-windows-wm.exe"}}')
    # up3 = Uploader('{"sysnum":"868608","up_from":{"fileId":"85236974150000","fpath":"F:/Java资料1（内部）.rar"},"up_to":{"fpath":"D:/Java资料1（内部）.rar"}}')
    # up4 = Uploader('{"sysnum":"868608","up_from":{"fileId":"85236974150000","fpath":"F:/AdobePhotoshopCS6.rar"},"up_to":{"fpath":"D:/AdobePhotoshopCS6.rar"}}')
    # time.sleep(3)
    # up.cancel()
    # down.suspend()
    # down1.suspend()
    # up1.suspend()
    time.sleep(10)
    # down.resume()


    # down1.resume()
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
