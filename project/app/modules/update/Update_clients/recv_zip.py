import os

import sys

from modules.update.Update_clients.update_client_log import logc


def recv_zip(update_scoket):
    """解压zip"""

    with open(r'version_update.zip', 'wb') as file:
        count = 0
        while True:
            try:
                data = update_scoket.recv(4096)
                # print('已接收到服务器zip数据 ：%s' % data)
                logc.info('----->已接收到服务器zip数据 ：%s' % data)
                if data:
                    file.write(data)
                    count += len(data)
                    file.flush()
                    # print("接收服务器zip完毕-文件大小为:%s"%str(os.path.getsize('E:/new_data.zip')))
                    logc.info("----->接收服务器zip完毕----文件大小为 : %s 字节" %str(os.path.getsize('E:/new_data.zip')))
                    logc.info('----->该文件存储的路径为：%s'% str(os.path.abspath(file.name)))
                else:
                    update_scoket.close()
                    file.close()
                    if count:
                        # print('文件传输完成')
                        logc.info('文件传输完成')
                    else:
                        # print('服务器没有这个文件')
                        logc.info('服务器没有这个文件')
                        break
                break
            except Exception as e:
                logc.error('》》》》接收zip出现异常：%s'% e)
    file.close()