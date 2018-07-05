import sys

from PyQt5.QtCore import QUrl

# from web import index
from PyQt5.QtGui import QIcon
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector
from PyQt5.QtWidgets import QApplication
from web import index
app = QApplication(sys.argv)
browser = QWebView()
browser.load(QUrl('qrc:/image/login.html'))
# browser.setWindowIcon(QIcon('C:/Users/zhongcun/Desktop/project/tests/imagers/logo.ico'))
# browser.setWindowIcon(QIcon('qrc:index.html'))
# browser.setPixmap(QPixmap("qrc:imagers/title01.png"))
browser.show()
# set = browser.settings()
# set.setAttribute(QWebSettings.DeveloperExtrasEnabled,True)
# inspector = QWebInspector()
# # inspector.setWindowFlags(Qt.WindowStaysOnTopHint)
# inspector.setPage(browser.page())
# inspector.show()
app.exec_()
