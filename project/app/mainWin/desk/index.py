import sys
import threading

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication
from pywin.mfc import thread

from mainWin.desk.service.platform import Platform

only_one_run = None
# notice_list = []

def start():
    global only_one_run
    if not only_one_run:
        only_one_run = Platform()
    only_one_run.show()
    # return only_one_run
    # print(only_one_run)

# def watch_list(item):
#     while True:
#         if len(notice_list)>0:
#             only_one_run


def add(item_content):
    print('--------------------'+item_content+str(only_one_run))
    # global only_one_run
    # if not only_one_run:
    #     only_one_run = Notification()

    # only_one_run.add(item_content)
    only_one_run.show()

if __name__ =="__main__":
    app = QApplication(sys.argv)
    start()
    # threading.Thread(target=add,args=('fdf',))
    only_one_run.show()
    sys.exit(app.exec_())