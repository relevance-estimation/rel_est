#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QListWidget, QTableWidget,
                            QHeaderView, QTableWidgetItem, QTableView)
from PyQt5.QtCore import QRect, Qt, QAbstractTableModel
from PyQt5.QtGui import QFont

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

        self.page = RelevantVideoResultPage(self)
        self.setCentralWidget(self.page)

        self.show()


class RelevantVideoResultPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.adEditBlock = QWidget(self)

        self.listWidget = QListWidget()

        self.listWidget.setMinimumSize(200, 500)
        self.listWidget.setMaximumWidth(200)

        self.table = QTableView()
        self.table.setMinimumSize(500, 300)
        #self.table.setColumnCount(4)
        #self.table.setRowCount(10)

        #self.table.setHorizontalHeaderLabels(["Имя файла", "Фрагмент", "Тип релевантности", "Оценка релевантности"])

        self.table.resizeColumnsToContents()

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        #self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.table.horizontalHeader().sectionSize(QHeaderView.Stretch)
        #self.table.resizeColumnsToContents()

        #self.table.setEditTriggers(QTableWidget.NoEditTriggers)


        self.table.showGrid()

        #for i in range(3): self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)

        self.pageHbox = QHBoxLayout()
        self.pageHbox.addWidget(self.listWidget)
        self.pageHbox.addWidget(self.table)

        self.adEditBlock.setMaximumSize(500, 250)

        self.adEditBlockVbox = QVBoxLayout()

        self.pageTitleLabel = QLabel("Релевантные видео")
        self.pageTitleLabel.setStyleSheet("""
            font: bold 18px;    
        """)
        self.pageTitleLabel.setAlignment(Qt.AlignCenter)

        self.pageVbox = QVBoxLayout(self)

        self.pageVbox.addWidget(self.pageTitleLabel)
        self.pageVbox.addLayout(self.pageHbox)

        self.setLayout(self.pageVbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
