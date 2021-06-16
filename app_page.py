import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from ad_edit_page import AdEditPage
from download_ad_page import DownloadAdPage
from download_video_page import DownloadVideoPage
#from analyze_page import AdEditPage
from relevant_moments_page import RelevantMoments
from relevant_video_page import RelevantVideoPage
from main_menu import MainMenu
from analyze_ad import AdAnalyzePage
from analyze_video import VidAnalyzePage

from functools import partial

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.center()
        self.signals()

    def initUI(self):
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()

        self.goToMenu = QtWidgets.QPushButton("Назад")
        self.goToMenu.setMaximumWidth(70)
        self.stacked_widget = QtWidgets.QStackedWidget()

        self.vbox.addWidget(self.goToMenu)
        self.vbox.addWidget(self.stacked_widget)

        self.widget.setLayout(self.vbox)

        self.setCentralWidget(self.widget)

        self.MainMenu = MainMenu(self)
        self.AdEditPage = AdEditPage(self)
        self.AdAnalyzePage = AdAnalyzePage(self)
        self.VidAnalyzePage = VidAnalyzePage(self)
        self.RelevantMoments = RelevantMoments(self)
        self.RelevantVideoPage = RelevantVideoPage(self)

        self.stacked_widget.addWidget(self.MainMenu)
        self.stacked_widget.addWidget(self.AdEditPage)
        self.stacked_widget.addWidget(self.AdAnalyzePage)
        self.stacked_widget.addWidget(self.VidAnalyzePage)
        self.stacked_widget.addWidget(self.RelevantMoments)
        self.stacked_widget.addWidget(self.RelevantVideoPage)

        self.setWindowTitle("Оценка релевантности видео")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_widget(self, widget):
        self.stacked_widget.setCurrentWidget(widget)
        self.setWindowTitle(widget.windowTitle())

    def signals(self):
        self.goToMenu.setVisible(False)
        self.stacked_widget.currentChanged.connect(self.goto)
        self.stacked_widget.setCurrentWidget(self.MainMenu)
        self.goToMenu.clicked.connect(partial(self.set_widget, self.MainMenu))

        self.main_menu_signals()

    def main_menu_signals(self):
        self.MainMenu.edit_keywords_slot(partial(self.set_widget, self.AdEditPage))
        self.MainMenu.ad_analyze_slot(partial(self.set_widget, self.AdAnalyzePage))
        self.MainMenu.video_analyze_slot(partial(self.set_widget, self.VidAnalyzePage))
        self.MainMenu.relevant_moments_slot(partial(self.set_widget, self.RelevantMoments))
        self.MainMenu.relevant_videos_slot(partial(self.set_widget, self.RelevantVideoPage))

    def goto(self, i):
        if self.stacked_widget.currentWidget() == self.MainMenu:
            self.goToMenu.setVisible(False)
        else:
            self.goToMenu.setVisible(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())