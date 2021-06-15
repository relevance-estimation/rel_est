#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                             QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QTextEdit, QFileDialog,
                             QMessageBox,QListWidget)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont, QTextOption
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

        self.page = DownloadVideoPage(self)
        self.setCentralWidget(self.page)

        self.show()


class DownloadVideoPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.UiComponents()
        self.signals()

    def UiComponents(self):
        self.adLinksBlock = QWidget()

        self.adLinksBlockVbox = QVBoxLayout()
        self.adLinksBlockHeader = QLabel("Ссылки на видео")
        self.vidLinksBlockText = QListWidget()
        self.adLinksBlockBrowse = QPushButton("Обзор")

        self.adLinksBlockVbox.addWidget(self.adLinksBlockHeader)
        self.adLinksBlockVbox.addWidget(self.vidLinksBlockText)
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
        self.savePathLabel = QLabel("")
        self.savePathLabel.setMaximumWidth(300)

        self.buttonsHbox.addWidget(self.savePathLabel)

        self.analysisHbox = QHBoxLayout()
        self.analysisHbox.setAlignment(Qt.AlignLeft)
        self.analysisHbox.setContentsMargins(0, 0, 0, 0)
        self.pageDownloadButton = QPushButton("Анализ")
        self.pageCancelButton = QPushButton("Отмена")
        self.pageDownloadInfo = QLabel("")
        self.pageDownloadInfo.setMaximumWidth(300)

        self.analysisHbox.addWidget(self.pageDownloadButton)
        self.analysisHbox.addWidget(self.pageCancelButton)
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

    def signals(self):
        self.pageCancelButton.setEnabled(False)
        self.adLinksBlockBrowse.clicked.connect(partial(self.loadFiles, self.vidLinksBlockText))

    def loadFiles(self, browseList):
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open files", "C\\Desktop")[0]
        if len(names) != 0:
            browseList.clear()
        for name in names:
            browseList.addItem(name)

    def browse_directory(self, label):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file != "":
            label.setText(file)

    def update_progress(self, progress):
        self.pageDownloadInfo.setText(progress)

    def start_analysis(self):
        self.pageDownloadButton.setEnabled(False)
        self.pageCancelButton.setEnabled(True)

    def cancel_analysis(self):
        self.pageDownloadButton.setEnabled(True)
        self.pageCancelButton.setEnabled(False)

    def start_analysis_slot(self, slot):
        self.pageDownloadButton.clicked.connect(slot)

    def cancel_slot(self, slot):
        self.pageCancelButton.clicked.connect(slot)

    def get_links(self):
        return self.vidLinksBlockText.toPlainText().split('\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
