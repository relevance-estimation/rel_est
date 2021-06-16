#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QFileDialog, QTableWidgetItem)
from PyQt5.QtCore import QRect, Qt, QAbstractTableModel
from PyQt5.QtGui import QFont
from relevant_video import RelevantVideo
from relevant_video_result_page import RelevantVideoResultPage

from functools import partial
import pandas as pd

class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


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
        self.layout.setContentsMargins(0, 0, 0, 0)

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

        self.tables = []

    def signals(self):
        self.tabs.setTabEnabled(1, False)
        self.tab1.buttonEdit.setEnabled(False)

        self.tab1.buttonVid.clicked.connect(partial(self.browse_and_check, self.tab1.pathVid))
        self.tab1.buttonRec.clicked.connect(partial(self.browse_and_check, self.tab1.pathRec))

        #self.tab1.buttonEdit.clicked.connect(self.launch_success)

        self.tab2.listWidget.itemSelectionChanged.connect(self.selectAd)
        #df = pd.DataFrame(data=[[1,2,3,4,5,6]])
        #self.load_df(df)

    def browse_and_check(self, browseList):
        self.loadFiles(browseList)
        if self.tab1.pathVid.count() != 0 and self.tab1.pathRec.count() != 0:
            self.tab1.buttonEdit.setEnabled(True)

    def loadFiles(self, browseList):
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open files", "C\\Desktop")[0]
        if len(names) != 0:
            browseList.clear()
        for name in names:
            browseList.addItem(name)

    def set_table(self, index):
        model = PandasModel(self.tables[index])
        self.tab2.table.setModel(model)

    def load_df(self, df):
        df.columns = ["Имя файла", "Фрагмент", "Тип релевантности", "Общая оценка", "Текст", "Цвета"]
        self.tables.append(df)

    def clear_tables(self):
        self.tables = []

    def load_data(self, df_list):
        self.clear_tables()
        for df in df_list:
            self.load_df(df)

    def selectAd(self):
        if len(self.tab2.listWidget.selectedIndexes()) != 0:
            self.set_table(self.tab2.listWidget.selectedIndexes()[0].row())
            self.tab2.table.showGrid()

    def launch_success(self):
        self.tabs.setTabEnabled(1, True)
        self.tab1.buttonEdit.setEnabled(False)
        self.tabs.setCurrentIndex(1)
        self.tab2.listWidget.clear()

        for i in range(self.tab1.pathRec.count()):
            self.tab2.listWidget.addItem(self.tab1.pathRec.item(i).text().split("/")[-1])

        self.tab2.listWidget.setCurrentRow(0)

    def start_analysis_slot(self, slot):
        self.tab1.buttonEdit.clicked.connect(slot)

    def get_ads(self):
        return [self.tab1.pathRec.item(i).text() for i in range(self.tab1.pathRec.count())]

    def get_vids(self):
        return [self.tab1.pathVid.item(i).text() for i in range(self.tab1.pathVid.count())]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
