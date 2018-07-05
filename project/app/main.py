# -*- coding: utf-8 -*-
import sys

import multiprocessing
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, qApp

# from mainWin.login.py.login import Client
from mainWin.tray.appTray import TrayIcon
from mainWin.desk import index as desk
from mainWin.login import index as login

#登录前
def beforeLogin():
    #系统登录
    login.start()


#登录后
def afterLogin():
    #启动托盘
    tray = TrayIcon()
    tray.show()

    #启动desk
    desk.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    beforeLogin()
    tray = TrayIcon()
    tray.show()



    #开启通知
    # notice = Notification()
    # notice.add("fsdfsdfsd")
    # notice.start()
    # add_list_up('[{"id":"1","up_from":"F:/eclipse-jee-kepler-SR2-win32.zip","up_to":"D:/eclipse-jee-kepler-SR2-win32.zip"}]')
    # notice.add("sdfsdfdsfsd")
    # connector = ConnectJs()
    # notice.webView.page().mainFrame().addToJavaScriptWindowObject("pyNotice", connector)


    sys.exit(app.exec_())