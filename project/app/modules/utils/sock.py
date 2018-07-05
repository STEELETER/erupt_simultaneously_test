from socket import *
import threading,os,time

from pip.backwardcompat import raw_input


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

    # def main(self):
    #     tcpCliSock=socket(AF_INET,SOCK_STREAM)
    #     tcpCliSock.connect(('127.0.0.1',9990))
    #     print ('connect server 9999 successfully !')
    #     cf = tcpCliSock.makefile('rw', 0)
    #     while 1:
    #         data=raw_input('>')
    #         try:
    #             if data:
    #                 cf.write(data+"\n")
    #                 data = cf.readline().strip()
    #                 if data:
    #                     print ("server say:",data)
    #                 else:
    #                     break
    #             else:
    #                 break
    #         except Exception as e:
    #             print ("send error,",str(e))

# if __name__ == "__main__":
#     cl = Client()
#     cl.main()
#
#
# if __name__ == "__main__" :
#     ser = Server()
#     ser.main()