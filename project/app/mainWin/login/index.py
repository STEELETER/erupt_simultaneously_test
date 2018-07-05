from common import context
from mainWin.login.py.client import Client


# only_one_run = None
# notice_list = []

def start():

    if not context.get('login'):
        context.set('login',Client())

    # global only_one_run
    # if not only_one_run:
    #     only_one_run = SysLogin()


