#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QFileDialog)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
from ad_edit_page_1 import AdEditPage1
from ad_edit_page_2 import AdEditPage2


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

        self.page = AdEditPage(self)
        self.setCentralWidget(self.page)

        self.show()


class AdEditPage(QWidget):
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
        self.tab1 = AdEditPage1(self.tabs)
        self.tab2 = AdEditPage2(self.tabs)

        # Add tabs
        self.tabs.addTab(self.tab1, "Загрузить")
        self.tabs.addTab(self.tab2, "Редактировать")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def signals(self):
        self.tabs.setTabEnabled(1, False)
        self.tab1.buttonEdit.setEnabled(False)
        self.tab1.buttonoverview.clicked.connect(self.browse_file)
        self.tab1.buttonEdit.clicked.connect(self.edit)

    def browse_file(self):
        select_file = QFileDialog.getOpenFileName(self)
        print(select_file)
        if select_file[0] != "":
            self.tab1.pathEdit.clear()
            self.tab1.pathEdit.insert(select_file[0])
            self.tab1.buttonEdit.setEnabled(True)

    def edit(self):
        self.tabs.setTabEnabled(1, True)
        self.tabs.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
