from common.conf import sysnum
from common.db import has


def check_sysnum(info):
    if int(info) == sysnum:
        return True
    else:
        raise Exception("外部非法请求！！")
