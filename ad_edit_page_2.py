#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit)
from PyQt5.QtCore import QRect, Qt
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

        self.page = AdEditPage2(self)
        self.setCentralWidget(self.page)

        self.show()


class AdEditPage2(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.adEditBlock = QWidget(self)

        self.adEditBlock.setMaximumSize(500, 250)

        self.adEditBlockVbox = QVBoxLayout()

        self.header = QLabel('<h1>Редактирование ключевых слов</h1>')
        self.header.setAlignment(Qt.AlignCenter)

        self.adEditBlockVbox.addStretch()
        self.adEditBlockVbox.addWidget(self.header)

        self.keywordsLabel = QLabel()
        self.keywordsLabel.setText('Ключевые слова:')
        self.keywordsEditLine = QLineEdit()
        self.keywordsHbox = QHBoxLayout()
        self.keywordsHbox.addWidget(self.keywordsLabel)
        self.keywordsHbox.addWidget(self.keywordsEditLine)

        self.adEditBlockVbox.addStretch()
        self.adEditBlockVbox.addLayout(self.keywordsHbox)

        self.saveAsButton = QPushButton("Сохранить как...")
        self.saveAsButton.setMaximumWidth(100)
        self.saveAsButtonHbox = QHBoxLayout()
        self.saveAsButtonHbox.addStretch(1)
        self.saveAsButtonHbox.addWidget(self.saveAsButton)

        self.adEditBlockVbox.addStretch()
        self.adEditBlockVbox.addLayout(self.saveAsButtonHbox)
        self.adEditBlockVbox.addStretch()
        self.adEditBlockVbox.setSpacing(30)

        self.adEditBlock.setLayout(self.adEditBlockVbox)

        self.pageVbox = QVBoxLayout(self)
        self.pageHbox = QHBoxLayout()
        self.pageHbox.addWidget(self.adEditBlock)
        self.pageVbox.addLayout(self.pageHbox)

        self.setLayout(self.pageVbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
