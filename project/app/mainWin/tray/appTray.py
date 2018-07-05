import os

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, qApp, QApplication

from modules.snspro.browser import chrome as snspro
from modules.trans import upload as trans
from modules.vdisk import mount as vdisk
from mainWin.desk import index as desk
from modules.about import index as about

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.__dir = os.path.dirname(os.path.abspath(__file__))
        self.showMenu()
        self.other()
        # self.show()

    def showMenu(self):
        print("showMenu..")

        #设计托盘的菜单
        self.menu = QMenu()
        # self.menu1 = QMenu()
        # browser = WebView()
        self.snspro_item = QAction("电子文档", self, triggered=snspro.start)
        self.snspro_item.setIcon(QIcon(self.__dir+'/icons/snspro.ico'))
        self.menu.addAction(self.snspro_item)

        self.trans_item = QAction("上传下载", self,triggered=trans.start)
        self.trans_item.setIcon(QIcon(self.__dir+'/icons/transfer.ico'))
        self.menu.addAction(self.trans_item)

        self.vdisk_item = QAction("挂盘", self,triggered=vdisk.start)
        self.vdisk_item.setIcon(QIcon(self.__dir+'/icons/vdisk.ico'))
        self.menu.addAction(self.vdisk_item)

        self.about = QAction("关于", self,triggered=about.start)
        # self.vdisk_item.setIcon(QIcon(self.__dir+'/icons/vdisk.ico'))
        self.menu.addAction(self.about)

        self.quitAction = QAction("退出", self, triggered=self.quit)
        self.quitAction.setIcon(QIcon(self.__dir+'/icons/exit.ico'))
        self.menu.addAction(self.quitAction)

        # self.menu1.addAction(self.showAction1)
        # self.menu1.addAction(self.showAction2)
        # self.menu.addMenu(self.menu1, )





        # self.menu1.setTitle("二级菜单")
        self.setContextMenu(self.menu)

    def other(self):
        # self.menu.triggered.connect(QtGui.)
        self.activated.connect(self.iconClied)
        #把鼠标点击图标的信号和槽连接
        self.messageClicked.connect(self.mClied)
        #把鼠标点击弹出消息的信号和槽连接
        self.setIcon(QIcon(self.__dir+'/icons/logo.ico'))
        self.icon = self.MessageIcon()
        #设置图标

    #def mousePressEvent (self,  event):
    #    print(event.pos())

    def iconClied(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            desk.start()
        # print('asdasdf')
        # self.event(self,)
            # print(self.event().pos())
            # self.menu.setGeometry(80,600,100,30)
            # self.menu.show()
            # self.menu
            # self.setContextMenu(self.menu)
           # reason = 1
            # self.contextMenu()
            # pw = self.parent()
            # if pw.isVisible():
            #     pw.hide()
            # else:
            #     pw.show()


    def mClied(self):
        self.showMessage("提示", "你点了消息", self.icon)

    def showM(self):
        pass
        # self.newWindow = SecondWindow()
        # self.newWindow.web.show()
        # self.newWindow.show()
        # self.showMessage("测试", "我是消息", self.icon)
        # app = QApplication(sys.argv)
        #
        # SecondWindow()
        # sys.exit(app.exec_())
    def guapan(self):
        pass
         # self.ex = FirstWindow()
         # self.ex.show()
    def quit(self):
        print('退出客户端...')
        "保险起见，为了完整的退出"
        self.setVisible(False)
        # self.parent().closeEvent
        qApp.quit()
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tray = TrayIcon()
    tray.show()
    tray.mClied()

    sys.exit(app.exec_())
