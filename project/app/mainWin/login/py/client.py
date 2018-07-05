#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys

import win32com.client
from common import context
from PyQt5.QtWebKitWidgets import QWebView

# import Channel

# from PyQt5 import QtWebEngine
# from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QWidget,QMainWindow,QApplication,QMessageBox,QLabel,QToolButton, QDesktopWidget,QPushButton,QGraphicsView,QGraphicsPixmapItem,QGraphicsScene,QGridLayout, QVBoxLayout,QHBoxLayout,QSpacerItem,QSizePolicy
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QPoint,QUrl,QCoreApplication,QSize,QMetaObject,QRect, QObject, pyqtSlot
from PyQt5.QtGui import QFont, QCursor,QPixmap,QPalette,QColor,QIcon,QPainter
from common import db

from common.unBorderWin.win import QUnFrameWindow
from mainWin.login.py.enter import Entry, get_lb_addr


class Client(QUnFrameWindow):
    def __init__(self):
        super(Client,self).__init__()
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        self.setStyleSheet(open(self.__dir+"/syslogin.qss").read())

        self.setFixedSize(356,356)
        self.setContentsMargins(8,8,8,8)
        self.label.setPixmap(QPixmap(self.__dir+"/title.png"))

        self.setCloseButton(True)
        self.setMinConfigButtons(True)
        self._ConfigButton.clicked.connect(self.setting)

        self.center()
        # self.show()
        self.setWindowIcon(QIcon(self.__dir+"/logo.ico"))
        self.setWindowTitle("中村电子文档安全管理系统V2.0")
        conn = Connector(self)
        self.webEngineView.page().mainFrame().javaScriptWindowObjectCleared.connect(lambda: self.webEngineView.page().mainFrame().addToJavaScriptWindowObject('external', conn))
        self.webEngineView.loadFinished.connect(self.show)

    #设置连接ip和port
    def setting(self):
        lb_addr = get_lb_addr()
        self.webEngineView.page().mainFrame().evaluateJavaScript("getParam('%s','%s','%s')"%(str(lb_addr[0]),str(lb_addr[1]),str(lb_addr[2])))

    def raise_error(self,msg):
        self.webEngineView.page().mainFrame().evaluateJavaScript("showErrMsg('%s')"%str(msg))

    # def success_close(self):
    #     self.close()



class Connector(QObject):

    def __init__(self,client):
        super(Connector,self).__init__()
        self.client = client
    #
    # @pyqtSlot()
    # def GetServerIp(self):
    #     return '172.21.1.152'
    #
    # @pyqtSlot()
    # def GetServerPort(self):
    #     return '172.21.1.152'
    #
    # @pyqtSlot()
    # def GetCaIp(self):
    #     return '172.21.1.152'

    @pyqtSlot(str,str,str)
    def SetServerInfo(self,ip,port,ca_ip):
        print(ip,port,ca_ip)
        data = {"server_ip":ip,"server_port":port,"ca_ip":ca_ip}

        if db.has("sys_param"):
            db.update_dict("sys_param",data)
        else:
            db.insert_dict("sys_param",data)

    #用户名密码登录
    @pyqtSlot(str,str)
    def LoginFromAccount(self,username,pwd):
        print(username,pwd)

        self.entry = Entry(uname=username,pwd=pwd)
        self.entry.abort.connect(self.client.raise_error)
        self.entry.start()



    #PIN码登录
    @pyqtSlot(str)
    def Login(self,pin):
        print(pin)
        store = win32com.client.Dispatch('CAPICOM.Store')
        store.Open(2, "my", 0)
        for cert in store.Certificates:
            print(cert.subjectName)
            print(cert.thumbprint)
            print(cert)

    #取消登录
    @pyqtSlot()
    def CancelLogin(self):
        print("取消登录")
        self.entry.terminate()



if __name__ == "__main__":



    import sys
    app = QApplication(sys.argv)

    # channeller = QWebChannel()
    # db_handler = Channel.dbHandler()
    # channeller.registerObject("db", db_handler)
    # file_handler = Channel.fileHandler()
    # channeller.registerObject("file", file_handler)
    # doc_handler = Channel.docHandler()
    # channeller.registerObject("doc", doc_handler)

    login = Client()
    login.show()


    # app.setStyleSheet(open("./syslogin.qss").read())
    #
    # window = QUnFrameWindow()
    # window.setFixedSize(356,356)
    # window.setContentsMargins(8,8,8,8)
    # window.label.setPixmap(QPixmap("title.png"))
    #
    # window.setCloseButton(True)
    # window.setMinConfigButtons(True)
    #
    # # window.center()
    # window.show()


    sys.exit(app.exec_())