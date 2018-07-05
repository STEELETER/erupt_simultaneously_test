import requests
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QWidget, QMessageBox, QDesktopWidget
from common import context


class WebView(QWidget):
    def __init__(self):
        super().__init__()
        self.get_client_home()
        self.create_client()

    def get_client_home(self):

        tomcat_addr = context.get("tomcat_addr")
        self.boot_url = "http://%s:%s/snspro/userController.do?linuxmainother"%(str(tomcat_addr[0]),str(tomcat_addr[1]))

        user_data = context.get("login_data")
        self.boot_args = {"a":user_data['uname'],"b":user_data['pwd'],"c":user_data['random2']}
        # response  = requests.post(url=set_url, data=args)
        # result = response.content.decode()

        # return result
        # print(result)
        # context.set("snspro_home",result)

    def create_client(self):
        # print(home)
        self.web = QWebView()



        req = QNetworkRequest()
        req.setUrl(QUrl(self.boot_url))
        # arr =  QByteArray()
        # arr.append(bytes(self.boot_args,encoding="utf-8"))
        self.web.load(req,QNetworkAccessManager.Operation,QByteArray(str(self.boot_args)))

        # self.web.load(QUrl('http://127.0.0.1:8080/snspro/shareFileController.do?boot_home'))
        # self.web.setHtml(home)
        self.web.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
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


