#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
from PyQt5 import QtWidgets

from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, pyqtSignal, QObject, pyqtSlot, QUrl
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication



class Platform(QWidget):

    def __init__(self):
        super(Platform, self).__init__()
        self._desktop = QApplication.instance().desktop()
        self.__dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__WebContent()
        self.__initPosition()
        self.__connectJs()
        print("启动desk")

    def __WebContent(self):
        self.resize(self._desktop.screenGeometry().width()/5, self._desktop.availableGeometry().height())
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.webView = QWebView()
        # BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        # new = os.path.join(BASE_DIR, 'web')
        #
        # new_file_name = os.path.join(new, 'noticeContent.html')
        # fname = 'file:///'+new_file_name
        # print(fname)
        # self.webView.load(QUrl('file:///C:/Users/Administrator/Desktop/app/mainWin/desk/web/desk.html'))
        print('file:///'+self.__dir+'/web/desk.html')
        self.webView.load(QUrl('file:///'+self.__dir+'/web/desk.html'))
        # self.webView.load(QUrl(fname))
        self.verticalLayout.addWidget(self.webView)
        # self.webView.loadFinished.connect(self.test)

    def onClose(self):
        #点击关闭按钮时
        self.isShow = False
        QTimer.singleShot(100, self.closeAnimation)#启动弹回动画

    def __initPosition(self):
        # 隐藏任务栏|去掉边框|顶层显示
        self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # 是否在显示标志
        self.isShow = True

        # 桌面
        # self._desktop = QApplication.instance().desktop()
        # 窗口初始开始位置
        self._startPos = QPoint(
            self._desktop.screenGeometry().width() ,
            self._desktop.availableGeometry().height()- self.height()
        )
        print(self._startPos)
        # 窗口弹出结束位置
        self._endPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() ,
            self._desktop.availableGeometry().height() - self.height()
        )
        print(self._endPos)
        # 初始化位置到右侧
        self.move(self._startPos)

        # 动画
        self.animation = QPropertyAnimation(self, b"pos")

        self.hide()  # 先隐藏
        super(Platform, self).show()


    def __connectJs(self):

        connector = ConnectJs(self)
        self.webView.page().mainFrame().javaScriptWindowObjectCleared.connect(lambda: self.webView.page().mainFrame().addToJavaScriptWindowObject('pyNotice', connector))

    def add(self,content=""):
        if content:
            self.__notice_list.insert(0,content)
            self.webView.page().mainFrame().evaluateJavaScript("pyNoticeAdd(%s)"%str(content))

    def show(self, title="", content=""):
        # 显示动画
        self.isShow = True
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self._endPos)
        self.animation.start()

    def closeAnimation(self):

        self.isShow = False
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self._startPos)
        self.animation.start()

class ConnectJs(QObject):
    def __init__(self,notice):
        super(ConnectJs, self).__init__()
        self.__notice =notice

    @pyqtSlot()
    def close(self):
        self.__notice.onClose()
       # controller.onClose()
       # controller.onClose()

#
# import sys
# from PyQt5.QtWidgets import QApplication, QHBoxLayout
# app = QApplication(sys.argv)
#
# notify = Notification()
# notify.show()






#




# sys.exit(app.exec_())