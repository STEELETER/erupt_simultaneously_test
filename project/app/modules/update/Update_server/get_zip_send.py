from modules.update.Update_server.Update_server_log import logs
from modules.update.Update_server.get_config import get_config
from modules.update.Update_server.send_zip import send_zip


def get_zip_send(conf_path,update_client,client_socket):
    """获取 zip 发送"""

    global update_z
    try:
        # 获取zip路径
        update_z = get_config(conf_path, update_client)
    except Exception as e:
        logs.info('----->获取zip路径出现异常：%s' % e)
        # print(e)
    # 根据路径 发送压缩包
    send_zip(update_z, client_socket)