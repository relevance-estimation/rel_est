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
        self.title = 'Оценка релевантности'
        self.left = 0
        self.top = 0
        self.width = 840
        self.height = 680
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.page = MainMenu(self)
        self.setCentralWidget(self.page)

        self.show()


class MainMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.menuBlock = QWidget(self)

        self.menuBlock.setMaximumSize(600, 700)



        self.downloadAdButton = QPushButton("Скачать рекламу")
        self.downloadVideoButton = QPushButton("Скачать видео")
        self.editKeywordsButton = QPushButton("Ключевые слова")
        self.relMomentsButton = QPushButton("Релевантные моменты")
        self.relVideosButton = QPushButton("Релевантные видео")
        self.channelAnalyticsButton = QPushButton("Анализ каналов")



        self.menuBlockVbox = QVBoxLayout()

        self.menuBlock.setStyleSheet("""
        QPushButton {
            font: 26px;
            min-height: 70px;
            min-width: 420px;
            }
        """)
        self.menuBlockVbox.setAlignment(Qt.AlignCenter)

        self.menuBlockVbox.addWidget(self.downloadAdButton)
        self.menuBlockVbox.addWidget(self.downloadVideoButton)
        self.menuBlockVbox.addWidget(self.editKeywordsButton)
        self.menuBlockVbox.addWidget(self.relMomentsButton)
        self.menuBlockVbox.addWidget(self.relVideosButton)
        self.menuBlockVbox.addWidget(self.channelAnalyticsButton)

        self.menuBlockVbox.setSpacing(30)

        self.menuBlock.setLayout(self.menuBlockVbox)

        self.pageVbox = QVBoxLayout(self)
        self.pageHbox = QHBoxLayout()
        self.pageHbox.addWidget(self.menuBlock)
        self.pageVbox.addLayout(self.pageHbox)

        self.setLayout(self.pageVbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())