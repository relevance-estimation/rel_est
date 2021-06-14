#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                             QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QTextEdit, QFileDialog)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont, QTextOption


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

        self.page = DownloadVideoPage(self)
        self.setCentralWidget(self.page)

        self.show()


class DownloadVideoPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.adLinksBlock = QWidget()

        self.adLinksBlockVbox = QVBoxLayout()
        self.adLinksBlockHeader = QLabel("Ссылки на видео")
        self.adLinksBlockText = QTextEdit()
        self.adLinksBlockText.setWordWrapMode(QTextOption.NoWrap)
        self.adLinksBlockBrowse = QPushButton("Обзор")

        self.adLinksBlockVbox.addWidget(self.adLinksBlockHeader)
        self.adLinksBlockVbox.addWidget(self.adLinksBlockText)
        self.adLinksBlockVbox.addWidget(self.adLinksBlockBrowse)

        self.adLinksBlock.setLayout(self.adLinksBlockVbox)
        self.adLinksBlockVbox.setContentsMargins(0, 0, 0, 0)

        self.pageTitleLabel = QLabel("Анализ видео")
        self.pageTitleLabel.setStyleSheet("""
            font: bold 18px;    
        """)

        self.pageTitleLabel.setAlignment(Qt.AlignCenter)

        self.pageDownloadButton = QPushButton("Анализ")
        self.pageDownloadInfo = QLabel("")

        self.buttonsHbox = QHBoxLayout()
        self.buttonsHbox.setAlignment(Qt.AlignLeft)
        self.buttonsHbox.setContentsMargins(0, 0, 0, 0)
        self.saveVideosToButton = QPushButton("Сохран. видео")
        self.savePathLabel = QLabel("")
        self.savePathLabel.setMaximumWidth(300)

        self.buttonsHbox.addWidget(self.saveVideosToButton)
        self.buttonsHbox.addWidget(self.savePathLabel)

        self.analysisHbox = QHBoxLayout()
        self.analysisHbox.setAlignment(Qt.AlignLeft)
        self.analysisHbox.setContentsMargins(0, 0, 0, 0)
        self.pageDownloadButton = QPushButton("Анализ")
        self.pageDownloadInfo = QLabel("")
        self.pageDownloadInfo.setMaximumWidth(300)

        self.analysisHbox.addWidget(self.pageDownloadButton)
        self.analysisHbox.addWidget(self.pageDownloadInfo)

        self.pageVbox = QVBoxLayout()
        self.pageVbox.addWidget(self.pageTitleLabel)
        self.pageVbox.addWidget(self.adLinksBlock)
        self.pageVbox.addLayout(self.buttonsHbox)
        self.pageVbox.addLayout(self.analysisHbox)

        self.setLayout(self.pageVbox)
        self.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                max-width: 80px;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
