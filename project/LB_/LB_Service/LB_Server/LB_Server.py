import socket
import threading

# 线程方法
from LB_.LB_Service.LB_Client.LB_Config import server_port
from LB_.LB_Service.LB_Server.LB_Handler import clock_clear, LB_Service
from LB_.LB_client.loggings import log


def threadings(client_socket, request_ip,local_ip):
    try:
        data = client_socket.recv(4096)
        #{'identity':'user','sysnum':'868608'}
        dict_data = eval(data)
        if  int(dict_data['sysnum']) == 868608:
            service = LB_Service()
            #客户端连接
            if dict_data['identity'] == 'user':
                log.info('<**********************real_user:'+str(request_ip)+'********************>')
                service.hand_user_req(client_socket,request_ip,local_ip)
                log.info('<******************************************************************************>')
            #服务器发送数据：
            elif dict_data['identity'] == 'client':
                print('<-----------------server_client:'+str(request_ip)+'-------------------->')
                service.hand_client_req(data,request_ip)
        else:
            log.info('此数据为非法数据！')
    except Exception as e:
        log.info('【lb-warn】接收数据|判断身份|建立service时出错![%s]'%str(e))
    finally:
        client_socket.close()



#开启lb-server服务
def server_start():
    #获取服务器本机ip
    local_ip = socket.gethostbyname(socket.gethostname())
    log.info( "[lb-info][%s]LB server start..."%str((local_ip,7100)))

    #建立lbserver端服务
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',server_port))
    s.listen(128)

    while True:
        client_socket,addr = s.accept()
        try:
            t = threading.Thread(target=threadings, args=(client_socket,addr,local_ip))
            t.start()
        except Exception as e:
            log.info('【lb-warn】连接有误![%s][%s]'%(str(addr),str(e)))
            log.info('【lb-warn】重新建立LB服务...')
            server_start()


#1.开启计时器
threading.Thread(target=clock_clear).start()

#2.开启lb-server服务
server_start()
















