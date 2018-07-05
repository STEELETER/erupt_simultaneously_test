from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QWidget, QMessageBox, QDesktopWidget


class WebView(QWidget):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        self.web = QWebView()
        self.web.load(QUrl('http://www.baidu.com'))
        # self.center()
        # self.web.show()
        self.web.closeEvent = self.closeEvent
        # pass
        # self.resize(300,300)
        # self.move(200,200)

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
                self.web.setVisible(False)
                # event.accept()

        #     else:
        #         event.ignore()
        # except:
        #     pass

def start():
    print('启动电子文档客户端...')
    view = WebView()
    view.center()
    view.web.show()


