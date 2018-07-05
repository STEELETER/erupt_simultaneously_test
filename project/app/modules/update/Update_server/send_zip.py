from modules.update.Update_server.Update_server_log import logs


def send_zip(update_z,client_socket):
    """根据路径发送 zip"""

    while True:
        try:
            with open(update_z, 'rb') as flie:
                data = flie.read(4096)
                # print(data)
                logs.info('----->读取配置zip数据为：%s' % data)
                if data is None:
                    break
                client_socket.send(data)
            # print('发送成功！！！')
            logs.info('----->发送成功！！！')
            break
        except Exception as e:
            # print('发送压缩包出现问题：%s' % e)
            logs.info('发送压缩包出现异常：%s' % e)
            break