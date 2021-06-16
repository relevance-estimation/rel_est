import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QFileDialog)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
from analyze_ad_page import AnalyzeAdPage
from download_ad_page import DownloadAdPage


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Редактирование рекламы'
        self.left = 0
        self.top = 0
        self.width = 840
        self.height = 680
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.page = AdAnalyzePage(self)
        self.setCentralWidget(self.page)

        self.show()


class AdAnalyzePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.setWindowTitle("Анализ рекламы")

    def initUI(self):
        self.UiComponents()
  #      self.signals()

    def UiComponents(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = AnalyzeAdPage(self.tabs)
        self.tab2 = DownloadAdPage(self.tabs)

        # Add tabs
        self.tabs.addTab(self.tab1, "Файлы с компьютера")
        self.tabs.addTab(self.tab2, "Файлы с Интернета")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())