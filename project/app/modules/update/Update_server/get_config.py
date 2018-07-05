import configparser

from modules.update.Update_server.Update_server_log import logs


def get_config(conf_path,update_client):
    """获取配置文件信息"""
    # conf_path = 'config.ini'
    try:
        cf = configparser.ConfigParser()
        cf.read(conf_path)  # 文件路径
        versions_str = cf.get("update", update_client)
        logs.info('----->已获取到配置文件中zip数据路径为：%s' % versions_str)
        # print('--1')
        # print(versions_str)
        return versions_str
    except Exception as e:
        # print(e)
        logs.error('》》》》获取配置文件出错 : %s' % e)

