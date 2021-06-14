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

        self.page = DownloadAdPage(self)
        self.setCentralWidget(self.page)

        self.show()


class DownloadAdPage(QWidget):
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

        self.adKeywordsBlock = QWidget()

        self.adKeywordsBlockVbox = QVBoxLayout()
        self.adKeywordsBlockHeader = QLabel("Ключевые слова")
        self.adKeywordsBlockText = QTextEdit()
        self.adKeywordsBlockText.setWordWrapMode(QTextOption.NoWrap)
        self.adKeywordsBlockBrowse = QPushButton("Обзор")

        self.adKeywordsBlockVbox.addWidget(self.adKeywordsBlockHeader)
        self.adKeywordsBlockVbox.addWidget(self.adKeywordsBlockText)
        self.adKeywordsBlockVbox.addWidget(self.adKeywordsBlockBrowse)

        self.adKeywordsBlock.setLayout(self.adKeywordsBlockVbox)
        self.adKeywordsBlockVbox.setContentsMargins(0, 0, 0, 0)

        self.pageHbox = QHBoxLayout()
        self.pageHbox.addWidget(self.adLinksBlock)
        self.pageHbox.addWidget(self.adKeywordsBlock)
        self.pageHbox.setSpacing(20)

        self.pageTitleLabel = QLabel("Скачивание рекламы")
        self.pageTitleLabel.setStyleSheet("""
            font: bold 18px;    
        """)

        self.pageTitleLabel.setAlignment(Qt.AlignCenter)

        self.pageDownloadButton = QPushButton("Скачать")
        self.pageDownloadInfo = QLabel("")

        self.pageVbox = QVBoxLayout()
        self.pageVbox.addWidget(self.pageTitleLabel)
        self.pageVbox.addLayout(self.pageHbox)
        self.pageVbox.addWidget(self.pageDownloadButton)
        self.pageVbox.addWidget(self.pageDownloadInfo)

        self.setLayout(self.pageVbox)

        self.setStyleSheet("""
            QPushButton {
                max-width: 80px;
            }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
