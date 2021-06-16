#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton,QMessageBox, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QFileDialog)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
from ad_edit_page_1 import AdEditPage1
from ad_edit_page_2 import AdEditPage2
import pickle


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

        self.page_controller = AdEditPageController(self.page)

        self.setCentralWidget(self.page)

        self.show()


class AdEditPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.setWindowTitle("Редактирование ключевых слов")

    def initUI(self):
        self.UiComponents()
        self.signals()

    def UiComponents(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

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

    def browse_file(self):
            select_file = QFileDialog.getOpenFileName(self)
            if select_file[0] != "":
                self.tab1.pathEdit.clear()
                self.tab1.pathEdit.insert(select_file[0])
                self.tab1.buttonEdit.setEnabled(True)

    def launch_success(self):
        self.tabs.setTabEnabled(1, True)
        self.tabs.setCurrentIndex(1)
        self.tab1.buttonEdit.setEnabled(False)

    def edit_slot(self, slot):
        self.tab1.buttonEdit.clicked.connect(slot)

    def get_file_path(self):
        return self.tab1.pathEdit.text()

    def put_keywords(self, keywords):
        self.tab2.keywordsEditLine.setText(keywords)

    def show_error(self, error):
        QMessageBox.critical(self,"Ошибка", error)

    def launch_fail(self):
        self.tab1.buttonEdit.setEnabled(False)

class AdEditPageController():
    def __init__(self, ad_edit_page):
        self.ad_edit_page = ad_edit_page
        self.signals()

    def signals(self):
        self.ad_edit_page.edit_slot(self.check_file)

    def check_file(self):
        try:
            filename = self.ad_edit_page.get_file_path()
            with open(filename, "rb") as f:
                vids = pickle.load(f)
        except:
            self.ad_edit_page.show_error("Ошибка при чтении файла")
            self.ad_edit_page.launch_fail()
            return
        try:
            keywords="".join(vids.videos[0].keywords)
            self.ad_edit_page.put_keywords(keywords)
            self.ad_edit_page.launch_success()
        except:
            self.ad_edit_page.show_error( "Ошибка доступа к ключевым словам")
            self.ad_edit_page.launch_fail()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
