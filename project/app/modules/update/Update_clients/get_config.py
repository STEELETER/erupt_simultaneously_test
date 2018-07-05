import configparser

from modules.update.Update_clients.update_client_log import logc


def get_config(conf_path):
    """获取配置文件信息"""
    # 获取配置文件 update 版本号
    # 配置文件
    try:
        cf = configparser.ConfigParser()
        cf.read(conf_path)  # 文件路径
        versions_str = cf.get("update", 'Revision')
        return versions_str
    except Exception as e:
        logc.info('》》》》获取配置文件信息出现异常：%s' % e)


