#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                             QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QTextEdit, QFileDialog,
                             QMessageBox, QListWidget)
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

        self.page = AnalyzVideoPage(self)
        self.setCentralWidget(self.page)

        self.show()


class AnalyzeVideoPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.UiComponents()
        self.signals()

    def UiComponents(self):
        self.adLinksBlock = QWidget()

        self.adLinksBlockVbox = QVBoxLayout()
        self.adLinksBlockHeader = QLabel("Пути к видео")
        self.adLinksBlockText = QListWidget()
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

        self.saveHbox = QHBoxLayout()
        self.saveHbox.setAlignment(Qt.AlignLeft)
        self.saveHbox.setContentsMargins(0, 0, 0, 0)
        self.saveToLabel = QLabel("Место сохранения: ")
        self.saveToButton = QPushButton("Обзор")
        self.chosenPathLabel = QLabel("")
        self.chosenPathLabel.setMaximumWidth(300)

        self.saveHbox.addWidget(self.saveToLabel)
        self.saveHbox.addWidget(self.saveToButton)
        self.saveHbox.addWidget(self.chosenPathLabel)

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
        self.pageVbox.addLayout(self.saveHbox)
        self.pageVbox.addWidget(self.adLinksBlock)
        self.pageVbox.addLayout(self.analysisHbox)

        self.setLayout(self.pageVbox)
        self.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                max-width: 80px;
            }
        """)

    def signals(self):
        self.pageDownloadButton.setEnabled(False)
        self.pageCancelButton.setEnabled(False)
        self.adLinksBlockBrowse.clicked.connect(partial(self.loadFiles, self.adLinksBlockText))
        self.saveToButton.clicked.connect(partial(self.browse_directory, self.chosenPathLabel))
        self.saveToButton.clicked.connect(self.analysis_check)

        self.adLinksBlockText.itemSelectionChanged.connect(self.analysis_check)

        self.pageDownloadButton.clicked.connect(self.start_analysis)
        self.pageCancelButton.clicked.connect(self.cancel_analysis)

    def read_file(self, textField):
        select_file = QFileDialog.getOpenFileName(self)
        if select_file[0] != "":
            try:
                with open(select_file[0], 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                textField.clear()
                for line in lines:
                    textField.insertPlainText(line)
            except:
                QMessageBox.critical(self, "Ошибка при чтении файла",
                                     "Убедитесь, что файл представляет собой текстовый документ")

    def browse_directory(self, label):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file != "":
            label.setText(file)

    def loadFiles(self, browseList):
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open files", "C\\Desktop")[0]
        if len(names) != 0:
            browseList.clear()
            for name in names:
                browseList.addItem(name)
            browseList.setCurrentRow(0)

    def update_progress(self, progress):
        self.pageDownloadInfo.setText(progress)

    def start_analysis(self):
        self.pageDownloadButton.setEnabled(False)
        self.pageCancelButton.setEnabled(True)
        self.saveToButton.setEnabled(False)
        self.adLinksBlockBrowse.setEnabled(False)
        self.adLinksBlockText.setEnabled(False)

    def cancel_analysis(self):
        self.pageDownloadButton.setEnabled(True)
        self.pageCancelButton.setEnabled(False)
        self.saveToButton.setEnabled(True)
        self.adLinksBlockBrowse.setEnabled(True)
        self.adLinksBlockText.setEnabled(True)

    def start_analysis_slot(self, slot):
        self.pageDownloadButton.clicked.connect(slot)

    def cancel_slot(self, slot):
        self.pageCancelButton.clicked.connect(slot)

    def get_links(self):
        return [self.adLinksBlockText.item(i).text() for i in range(self.adLinksBlockText.count())]

    def get_save_info_path(self):
        return self.chosenPathLabel.text()

    def check_size(self):
        return self.adLinksBlockText.count() > 0

    def analysis_check(self):
        if self.check_size() and self.chosenPathLabel.text() != "":
            self.pageDownloadButton.setEnabled(True)
        else:
            self.pageDownloadButton.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
