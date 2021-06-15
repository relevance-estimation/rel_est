import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from ad_edit_page import AdEditPage
from download_ad_page import DownloadAdPage
from download_video_page import DownloadVideoPage
#from analyze_page import AdEditPage
from relevant_mom import RelevantMoments
from relevant_video_page import RelevantVideoPage
from main_menu import MainMenu



class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.center()


        self.m_pages = {}

        self.register(MainMenu(self), "main")
        self.register(AdEditPage(self), "adEditPage")
        self.register(DownloadAdPage(self), "DownloadAdPage")
        self.register(DownloadVideoPage(self), "DownloadVideoPage")
        self.register(RelevantMoments(self), "RelevantMoments")
        self.register(RelevantVideoPage(self), "RelevantVideoPage")


        self.goto("main")

        #self.dowloadAdButton.clicked.connect(self.make_handleButton("adEditPage"))

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())