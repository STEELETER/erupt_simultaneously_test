import json
import threading
import socket
import os,sys

from modules.utils.conf import trans_per_size, sysnum
from modules.utils.log import log


#上传文件
from common.sock import socket_send_json, socket_recv_dict


def recv_file(client_socket, data, request_ip, local_ip):

     #在服务器上生成所上传的文件
    def make_file(has_recv):
         log.info("[trans-info]服务器开始创建[%s]文件..."%str(fpath))
         with open(tmp_path, 'wb') as f:
            f.seek(has_recv)  # 定位到已经传到的位置
            while has_recv < int(fsize):
                data = client_socket.recv(trans_per_size)
                if not data:
                    break
                else:
                    f.write(data)
                    has_recv += len(data)

         has_recv = os.path.getsize(tmp_path) # 计算文件大小
         if int(has_recv)==int(fsize):
            os.rename(tmp_path,fpath)
            log.info("[trans-info]服务器已生成[%s]文件,大小为%s，与原文件大小一致"%(str(fpath),str(fsize)))
            return_info(has=has_recv,finish="True")
         else:
            os.remove(tmp_path)
            log.info("【trans-warn】服务器已生成[%s]文件,大小为%s,与原文件大小不一致！%s"%(str(fpath),str(fsize)))
            return_info(has=has_recv,finish="")


    def return_info(has,finish):
        info = {"has":str(has),"finish":str(finish)}
        log.info("[trans-info]发送到客户端%s的服务器相关文件数据:%s"%(str(request_ip),str(info)))
        socket_send_json(client_socket,info)

    try:
        fsize = data['fsize']
        fpath = data['fpath']
        tmp_path = "%s.tmp"%str(fpath)

        #已经完整存在
        if os.path.exists(fpath):
             log.info("[trans-info][%s]文件已完整存在,下面验证大小是否一致..."%str(fpath))
             has_recv = os.path.getsize(fpath) # 计算文件大小

             if int(has_recv) == int(fsize):
                 log.info("[trans-info][%s]文件与待上传文件大小一致：V"%str(fpath))
                 return_info(has=has_recv,finish="True")
             else:
                log.info("[trans-info][%s]文件与待上传文件大小不一致：X"%str(fpath))
                os.remove(fpath)
                return_info(has=0,finish="")  #""空字符串为False
                make_file(has_recv)

        #为temp临时文件，上传了一部分
        elif os.path.exists(tmp_path):
            has_recv = os.path.getsize(tmp_path) # 计算文件大小
            log.info("已上传比例：%s"%str(has_recv%trans_per_size))
            log.info("[trans-info][%s]文件已存在临时上传文件,大小为%s"%(str(tmp_path),str(has_recv)))
            return_info(has=has_recv,finish="")
            make_file(has_recv)

        #第一次上传
        else:
            log.info("[trans-info][%s]文件未上传过此文件.即将上传..."%str(fpath))
            has_recv = 0
            return_info(has=has_recv,finish="")
            make_file(has_recv)
    except Exception as e:
        log.info('【trans-warn】%s上传至服务器%s的文件发生错误！[%s]'%(str(request_ip),str(fpath),str(e)))

#删除服务器上正在上传的文件
def del_file(client_socket, data,request_ip,local_ip):
    try:
        tmpfile = data['fpath']+".tmp"
        if os.path.exists(tmpfile):
            os.remove(tmpfile)
    except Exception as e:
        pass

#下载文件
def down_file(client_socket, data, request_ip, local_ip):

    #回传文件信息
    def return_info(exist,fsize):
        info = {"exist":str(exist),"fsize":str(fsize)}
        log.info("[trans-info]发送到客户端%s的服务器相关文件数据:%s"%(str(request_ip),str(info)))
        socket_send_json(client_socket,info)

    #下载文件
    def send_file(has_down):
        with open(fpath, 'rb') as f:
            f.seek(has_down)  # 定位到已经传到的位置
            while has_down < int(fsize):
                data = f.read(trans_per_size)
                client_socket.send(data)
                has_down += len(data)

    fpath = data['fpath']
    has_down = int(data['has_down'])


    #不存在该文件
    if not os.path.exists(fpath):
        return_info(exist="",fsize="0")
    else:
        fsize = os.path.getsize(fpath)
        if int(fsize) == 0:
            return_info(exist="",fsize="0")
        else:
            return_info(exist="True",fsize=fsize)
            send_file(has_down)






def server_start():

    #获取服务器本机ip
    local_ip = socket.gethostbyname(socket.gethostname())
    log.info( "[trans-info][%s]trans server start..."%str((local_ip,7000)))

    # 建立tans服务socket
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_socket.bind(('', 7000))
    serv_socket.listen(128)

    while True:
        try:
            # b 接受客户端的连接请求
            client_socket,addr = serv_socket.accept()

            try:
                result = socket_recv_dict(client_socket)
                log.info("<-------------------------:%s------------------------>" %str(addr))
                log.info("[trans-info]接收到的请求数据：%s" %str(result))

                order = result['order']
                if order == "add":
                    service = recv_file
                elif order == "del":
                    service = del_file
                elif order == "down":
                    service = down_file

                #开启线程
                t = threading.Thread(target=service, args=(client_socket,result,addr,local_ip))
                t.start()
            except Exception as e:
                log.info('【trans-warn】接收的数据格式有误![%s]'%str(e))
                socket_send_json(client_socket,"")

        except Exception as e:
            log.info('【trans-warn】连接有误![%s][%s]'%(str(addr),str(e)))
            log.info('【trans-warn】重新建立trans服务...')
            server_start()


if __name__ == '__main__':
    server_start()
