import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *

# class Form(QWidget):
#
#     def __init__(self, parent=None):
#
#         super(Form, self).__init__(parent)
#
#         tmp = QWebView()
#         buttonLayout1 = QVBoxLayout()
#         buttonLayout1.addWidget(tmp)
#         mainLayout = QGridLayout()
#         mainLayout.addLayout(buttonLayout1, 1, 1)
#         self.setWindowIcon(QIcon("qrc:/imagers/155.jpg"))
#
#         # self.setWindowTitle("C:/Users/zhongcun/Desktop/project/tests/imagers/155.jpg")
#         # self.setWindowIconText("C:/Users/zhongcun/Desktop/project/tests/imagers/155.jpg")
#         self.setLayout(mainLayout)
#
#         tmp.load(QUrl('qrc:/imagers/images.html'))
#         tmp.show()
#
# from docx import Document
# if __name__ == '__main__':
#     document = Document()
#
#     import sys
#     app = QApplication(sys.argv)
#     screen = Form()
#     screen.show()
#     sys.exit(app.exec_())
# import sys
# def Imzing():
#     app = QApplication(sys.argv)
#     app.setWindowIcon(QIcon("qrc:/imagers/155.jpg"))
#     app.show()
#     app.exit(app.exec_())
# import sys

# file = QtCore.QFile('css.qss')
# file.open(QtCore.QFile.ReadOnly)
# styleSheet = file.readAll()
# styleSheet = unicode(styleSheet, encoding='utf8')
# QtGui.qApp.setStyleSheet(styleSheet)

from tests import doc
app = QApplication(sys.argv)

browser = QWebView()
browser.load(QUrl('file:///C:/Users/zhongcun/Desktop/project/tests/doc.py'))
# browser.setWindowIcon(QIcon('C:/Users/zhongcun/Desktop/project/tests/imagers/logo.ico'))
browser.setWindowIcon(QIcon(':images.html'))
# browser.setPixmap(QPixmap("qrc:imagers/title01.png"))

browser.show()

app.exec_()


# from docx import Document
# from docx.shared import Inches
# from tests.test2 import doc
# document = Document("qrc:/default.docx")
#
# document.add_heading('Document Title', 0)
#
# p = document.add_paragraph('A plain paragraph having some ')
# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True
#
# document.add_heading('Heading, level 1', level=1)
# document.add_paragraph('Intense quote', style='IntenseQuote')
#
# document.add_paragraph(
#     'first item in unordered list', style='ListBullet'
# )
# document.add_paragraph(
#     'first item in ordered list', style='ListNumber'
# )
#
# document.add_page_break()
#
# document.save('C:/Users/zhongcun/Desktop/demo.docx')
