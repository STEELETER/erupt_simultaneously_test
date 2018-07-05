from modules.utils.conf import sysnum
from modules.utils.db import has


def check_sysnum(info):
    if str(info) == sysnum:
        return True
    else:
        raise Exception("外部非法请求！！")
