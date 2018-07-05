import json
from socket import *
import threading,os,time

import struct
from pip.backwardcompat import raw_input

from common.check import check_sysnum
from common.conf import sysnum


class Server():
    def __init__(self,ip='',port=9999):
        try:
            addr=(ip,port)
            self.socket=socket(AF_INET,SOCK_STREAM)
            self.socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
            self.socket.bind(addr)
            self.socket.listen(128)
        except Exception as e :
            print('ip or port error :',str(e))
            self.socket.close()

    def run(self):
        while 1 :
            try :
                print( 'wait for connecting ...')
                tcpCliSock,addr = self.tcpSerSock.accept()
                addrStr = addr[0]+':'+str(addr[1])
                print ('connect from',addrStr)
            except KeyboardInterrupt:
                self.close=True
                tcpCliSock.close()
                self.tcpSerSock.close()
                print ('KeyboardInterrupt')
                break
            ct = ClientThread(tcpCliSock,addrStr)
            ct.start()

class ClientThread(threading.Thread):
    def __init__(self,tcpClient,addr):
        super(ClientThread,self).__init__()

        self.tcpClient = tcpClient
        self.addr = addr
        self.timeout = 60
        tcpClient.settimeout(self.timeout)
        self.cf = tcpClient.makefile('rw',0)

    def start(self):
        while 1:
            try:
                data = self.cf.readline().strip()
                if data:
                    if data.find("set time")>=0:
                        self.timeout = int(data.replace("set time ",""))
                        self.tcpClient.settimeout(self.timeout)
                    print(self.addr,"client say:",data)
                    self.cf.write(str(self.addr)+" recevied ok!"+"\n")
                else:
                    break
            except Exception as e:
                self.tcpClient.close()
                self.cf.write("time out !"+"\n")
                print (self.addr,"send message error,",str(e))
                break

#客户端socket
class Soc_client():
    def __init__(self,addr):
        try:
            self.socket = socket(AF_INET,SOCK_STREAM)
            self.socket.connect(addr)
        except Exception as e:
            print('建立socket客户端失败：%s'%str(e))
            self.socket.close()
            self.socket = None
            raise Exception("建立socket客户端失败")

#socket通信前封装包头包体
def socket_send_json(tcp_socket,data_str):
    data_body = json.dumps(data_str).encode()
    body_len = len(data_body)

    #报文头
    data_head = struct.pack("2i",sysnum,body_len)
    tcp_socket.sendall(data_head + data_body)

#socket通信之间解析包头和包体
def socket_recv_dict(tcp_socket):
    #接收报文头
    body_head = tcp_socket.recv(8)
    sysnum,body_len = struct.unpack("2i",body_head[:8])

    #验证请求
    check_sysnum(sysnum)

    #接收报文体
    recv_data = tcp_socket.recv(body_len)
    data_dict = json.loads(recv_data.decode())
    return data_dict
