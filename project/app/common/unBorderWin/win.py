#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys

from PyQt5.QtWebKitWidgets import QWebView

# import Channel

# from PyQt5 import QtWebEngine
# from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QWidget,QMainWindow,QApplication,QMessageBox,QLabel,QToolButton, QDesktopWidget,QPushButton,QGraphicsView,QGraphicsPixmapItem,QGraphicsScene,QGridLayout, QVBoxLayout,QHBoxLayout,QSpacerItem,QSizePolicy
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QPoint,QUrl,QCoreApplication,QSize,QMetaObject,QRect
from PyQt5.QtGui import QFont, QCursor,QPixmap,QPalette,QColor,QIcon,QPainter


global movenum


class QTitleLabel(QLabel):

    """
    新建标题栏标签类
    """
    def __init__(self, *args):
        super(QTitleLabel, self).__init__(*args)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class QTitleButton(QPushButton):
    """
    新建标题栏按钮类
    """
    def __init__(self, *args):
        super(QTitleButton, self).__init__(*args)
        self.setFont(QFont("Webdings")) # 特殊字体以不借助图片实现最小化最大化和关闭按钮
        self.setFixedWidth(36)




class QUnFrameWindow(QWidget):
    """
    无边框窗口类
    """
    def __init__(self):
        super(QUnFrameWindow, self).__init__(None,Qt.FramelessWindowHint) # 设置为顶级窗口，无边框
        # self._padding =8 # 设置边界宽度为8
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.SHADOW_WIDTH = 8
        self.initLayout() # 设置框架布局
        #self.setMinimumSize(900,700)
        self.setMouseTracking(True) # 设置widget鼠标跟踪
        self.initDrag() # 设置鼠标跟踪判断默认值
        self.center()
        self.__dir = os.path.dirname(os.path.abspath(__file__))



    #绘制边框阴影
    def drawShadow(self,painter):
        #print('ddddddddddddddddddd')
        #绘制左上角、左下角、右上角、右下角、上、下、左、右边框

        self.pixmaps=[self.__dir+'/shadow/shadow_left_top.png',self.__dir+'/shadow/shadow_left_bottom.png',self.__dir+'/shadow/shadow_right_top.png',self.__dir+'/shadow/shadow_right_bottom.png',self.__dir+'/shadow/shadow_top.png',self.__dir+'/shadow/shadow_bottom.png',self.__dir+'/shadow/shadow_left.png',self.__dir+'/shadow/shadow_right.png']
        painter.drawPixmap(0, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[0]))   #左上角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[2]))   #右上角
        painter.drawPixmap(0,self.height()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[1]))   #左下角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[3]))  #右下角
        painter.drawPixmap(0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH, QPixmap(self.pixmaps[6]).scaled(self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH)) #左
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH, QPixmap(self.pixmaps[7]).scaled(self.SHADOW_WIDTH, self.height()- 2*self.SHADOW_WIDTH)) #右
        painter.drawPixmap(self.SHADOW_WIDTH, 0, self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[4]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH)) #上
        painter.drawPixmap(self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[5]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH))   #下


    def paintEvent(self, event):
        painter = QPainter(self)

        self.drawShadow(painter)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawRect(QRect(self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.width() - 2 * self.SHADOW_WIDTH,
                               self.height() - 2 * self.SHADOW_WIDTH))


    def initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False


    def initLayout(self):
        # 设置框架布局


        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setWindowIcon(QIcon('logo.ico'))

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(8,8,8,8)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")


        #添加竖排layout
        self.verticalLayout =QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout,0,0,0,0)


        self.label = QTitleLabel()
        self.label.setScaledContents(False)
        # self.label.setPixmap(QPixmap("title.png"))

        #
        # sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        # self.label.setSizePolicy(sizePolicy)


        self.label.setFixedHeight(108)
        self.label.setContentsMargins(0,0,0,0)
        self.label.setMouseTracking(True)

        self.verticalLayout.addWidget(self.label)
        #在横排layput中添加按钮


        #在上方横排下排生成一个横排放浏览器
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0,0,0,0)#浏览器右下方留出拖拽空间
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)


        #生成一个浏览器组件，添加到下方的横排layout
        self.webEngineView = QWebView()
        self.webEngineView.load(QUrl('file:///C:/Users/zhongcun/Desktop/project/app/mainWin/login/web/login.html'))

        self.webEngineView.setObjectName('webEngineView')

                         #---------------------------------------------------
        # self.webEngineView.page().setWebChannel(channeller)

        self.webEngineView.setContentsMargins(0,0,0,0)

        self.webEngineView.setMaximumSize(QSize(10000, 10000))
        self.webEngineView.setMouseTracking(True)
        self.horizontalLayout.addWidget(self.webEngineView)


    def setCloseButton(self, bool):
        # 给widget定义一个setCloseButton函数，为True时设置一个关闭按钮
        if bool == True:
            self._CloseButton = QTitleButton(b'\xef\x81\xb2'.decode("utf-8"), self)
            self._CloseButton.setObjectName("CloseButton") # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._CloseButton.setToolTip("关闭")
            self._CloseButton.setMouseTracking(True) # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._CloseButton.setFixedHeight(36)

            #self._CloseButton.setFixedHeight(self._TitleLabel.height()) # 设置按钮高度为标题栏高度
            self._CloseButton.clicked.connect(self.close) # 按钮信号连接到关闭窗口的槽函数


    def setMinConfigButtons(self, bool):
        # 给widget定义一个setMinMaxButtons函数，为True时设置一组最小化最大化按钮
        if bool == True:
            self._MinimumButton = QTitleButton(b'\xef\x80\xb0'.decode("utf-8"), self)
            self._MinimumButton.setObjectName("MinMaxButton") # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MinimumButton.setToolTip("最小化")
            self._MinimumButton.setMouseTracking(True) # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MinimumButton.setFixedHeight(36)  # 设置按钮高度为标题栏高度
            #self._MinimumButton.setFixedHeight(self._TitleLabel.height()) # 设置按钮高度为标题栏高度
            self._MinimumButton.clicked.connect(self.showMinimized) # 按钮信号连接到最小化窗口的槽函数
            self._ConfigButton = QTitleButton(b'\xef\x81\x80'.decode("utf-8"), self)
            self._ConfigButton.setObjectName("MinMaxButton") # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._ConfigButton.setToolTip("设置")
            self._ConfigButton.setMouseTracking(True) # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._ConfigButton.setFixedHeight(36)


    def resizeEvent(self, QResizeEvent):

        try:
            self._CloseButton.move(self.width() - self._CloseButton.width()-16, 16)
        except:
            pass
        try:
            self._MinimumButton.move(self.width() - (self._CloseButton.width() + 1) * 2 -16+2, 16)
        except:
            pass
        try:
            self._ConfigButton.move(self.width() - (self._CloseButton.width() + 1) * 3 -16+3, 16)
        except:
            pass

    def mousePressEvent(self, event):

        # 重写鼠标点击的事件

        if (event.button() == Qt.LeftButton) and (event.y() < self.label.height()+16):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):

        if (Qt.LeftButton and self._move_drag):
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            #window.setContentsMargins(0,0,0,0) #动态调整阴影
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False


    #窗口居中
    def center(self):
        qr = self.frameGeometry()  # 获得主窗口的一个矩形特定几何图形。这包含了窗口的框架。
        cp = QDesktopWidget().availableGeometry().center()  # 算出相对于显示器的绝对值。
        # 并且从这个绝对值中，我们获得了屏幕中心点。
        qr.moveCenter(cp)  # 矩形已经设置好了它的宽和高。现在我们把矩形的中心设置到屏幕的中间去。
        # 矩形的大小并不会改变。
        self.move(qr.topLeft())  # 移动了应用窗口的左上方的点到qr矩形的左上方的点，因此居中显示在我们的屏幕


    def closeEvent(self, event):
        # try:
        #     reply = QMessageBox.question(self, '提示',
        #                                  "确认退出?", QMessageBox.Yes, QMessageBox.No)
        #     print(reply == QMessageBox.Yes)
        #     if reply == QMessageBox.Yes:
                event.ignore()
                # self.setVisible(False)
                print('---------')
                self.setVisible(False)
                # event.accept()

        #     else:
        #         event.ignore()
        # except:
        #     pass

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


    app.setStyleSheet(open("./syslogin.qss").read())
    window = QUnFrameWindow()
    window.setFixedSize(356,356)
    window.setContentsMargins(8,8,8,8)

    window.setCloseButton(True)
    window.setMinConfigButtons(True)

    window.show()


    sys.exit(app.exec_())