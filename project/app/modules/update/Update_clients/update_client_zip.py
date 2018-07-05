from modules.update.Update_clients.recv_zip import recv_zip
from modules.update.Update_clients.update_client_log import logc


def update_client_zip(update_scoket,update):
    """客户端第二次请求server zip"""
    try:
        update_scoket.send(update.encode())
        logc.info('----->发送获取更新包请求成功！')
        # print('发送获取 跟新包请求成功!')
        # 接收服务器zip 写入文件中
        recv_zip(update_scoket)
    except Exception as e :
        logc.error('》》》》client端第二次请求更新包请求出现异常：%s' % e)
        # print( 'client发送第二次请求更新包请求出现异常-：%s'% e )
        update_scoket.close()

