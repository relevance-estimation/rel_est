#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QFileDialog)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
from relevant_video import RelevantVideo
from relevant_video_result_page import RelevantVideoResultPage

from functools import partial

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

        self.page = RelevantVideoPage(self)
        self.setCentralWidget(self.page)

        self.show()


class RelevantVideoPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.UiComponents()
        self.signals()

    def UiComponents(self):
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = RelevantVideo(self.tabs)
        self.tab2 = RelevantVideoResultPage(self.tabs)

        # Add tabs
        self.tabs.addTab(self.tab1, "Загрузить")
        self.tabs.addTab(self.tab2, "Анализ")


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    def signals(self):
        self.tabs.setTabEnabled(1, False)
        self.tab1.buttonEdit.setEnabled(False)

        self.tab1.buttonVid.clicked.connect(partial(self.browse_and_check, self.tab1.pathVid))
        self.tab1.buttonRec.clicked.connect(partial(self.browse_and_check, self.tab1.pathRec))

    def browse_and_check(self, browseList):
        self.loadFiles(browseList)
        if self.tab1.pathVid.count() != 0 and self.tab1.pathRec.count() != 0:
            self.tab1.buttonEdit.setEnabled(True)

    def loadFiles(self, browseList):
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open files", "C\\Desktop")[0]
        for name in names:
            browseList.addItem(name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
