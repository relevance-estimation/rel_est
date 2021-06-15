import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QFileDialog)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
from analyze_video_page import AnalyzVideoPage
from download_video_page import DownloadVideoPage


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Редактирование видео'
        self.left = 0
        self.top = 0
        self.width = 840
        self.height = 680
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.page = AdPageAnaliz(self)
        self.setCentralWidget(self.page)

        self.show()


class AdPageAnaliz(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.UiComponents()
  #      self.signals()

    def UiComponents(self):
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = AnalyzVideoPage(self.tabs)
        self.tab2 = DownloadVideoPage(self.tabs)

        # Add tabs
        self.tabs.addTab(self.tab1, "Ссылки на видео(компьютер)")
        self.tabs.addTab(self.tab2, "Ссылки на видео(интернет)")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())