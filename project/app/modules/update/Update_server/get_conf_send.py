from modules.update.Update_server.Update_server_log import logs
from modules.update.Update_server.get_config import get_config


def get_conf_send(conf_path,update_client,client_socket):
    """获取配置文件且发送"""
    global update_num
    try:
        # 读取配置文件 获取 版本号 返回
        update_num = get_config(conf_path, update_client)
        # logs.info('----->已读取到配置文件数据：%s' % update_num)
        # print('已读到配置文件数据：%s' % update_num)
    except Exception as e:
        # print(e)
        logs.info('》》》》读取配置文件数据异常：%s' % e)
    try:
        client_socket.send(update_num.encode())
        logs.info('----->已将读取到配置文件中的数据发送成功！')
    except Exception as e:
        # print('发送数据出现异常：%s' % e)
        logs.info('》》》》发送数据异常：%s' % e)
    # print('已将读取到配置文件中的版本号发送！')
