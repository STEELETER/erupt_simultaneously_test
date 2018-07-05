from urllib import request

from LB_.LB_client.loggings import log


def test_tomcat_ip(data_str):
    """测试tomcat_ip"""
    global connect_num, real_ip_list

    # 读取配置文件中的ip
    from LB_.LB_client.LB_Config import get_random_ip
    try:
        real_ip_list = get_random_ip()
        # log.error('----->读取配置文件出错！')i
        log.info('-----》已获取到配置文件列表:%s' % real_ip_list)
    except Exception as e:
        log.error('----->获取配置文件ip出错:%s'% e)
        return False
    # 遍历出配置文件中ip 拿着这个ip 直接连接tomcat 看看是否有返回值 如果返回值为 None 或者为“”
    for i in real_ip_list:
        # 连接tomcat 将能连通tomcat的ip返回
        try:
            tomcat_url = 'http://' + i + ':8080/snspro/getConnNum'
            log.info("-----》user_client访问tomcat目标地址：%s" % str(tomcat_url))
            connect_num = request.urlopen(tomcat_url)
            connect_num = connect_num.read().decode()
            log.info('-----》获取到tomcat的数据：%s' % str(connect_num))
        except Exception as e:
            log.error('----->连接tomcat出现错误%s'% e)
            return False
        if connect_num is not None or '':
            return i
