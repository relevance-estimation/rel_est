#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QTextEdit, QFileDialog,
                            QMessageBox)
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

        self.page = DownloadAdPage(self)
        self.setCentralWidget(self.page)

        self.show()


class DownloadAdPage(QWidget):
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

        self.pageTitleLabel = QLabel("Анализ рекламы")
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
        self.pageCancelButton = QPushButton("Отмена")
        self.pageDownloadInfo = QLabel("")
        self.pageDownloadInfo.setMaximumWidth(300)

        self.analysisHbox.addWidget(self.pageDownloadButton)
        self.analysisHbox.addWidget(self.pageCancelButton)
        self.analysisHbox.addWidget(self.pageDownloadInfo)

        self.pageVbox = QVBoxLayout()
        self.pageVbox.addWidget(self.pageTitleLabel)
        self.pageVbox.addLayout(self.saveHbox)
        self.pageVbox.addLayout(self.pageHbox)
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
        self.pageDownloadButton.setEnabled(False)
        self.pageCancelButton.setEnabled(False)
        self.adLinksBlockBrowse.clicked.connect(partial(self.read_file, self.adLinksBlockText))
        self.adKeywordsBlockBrowse.clicked.connect(partial(self.read_file, self.adKeywordsBlockText))
        self.saveVideosToButton.clicked.connect(partial(self.browse_directory, self.savePathLabel))
        self.saveToButton.clicked.connect(partial(self.browse_directory, self.chosenPathLabel))
        self.saveToButton.clicked.connect(self.analysis_check)

        self.adLinksBlockText.textChanged.connect(self.analysis_check)
        self.adKeywordsBlockText.textChanged.connect(self.analysis_check)

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

    def update_progress(self, progress):
        self.pageDownloadInfo.setText(progress)

    def start_analysis(self):
        self.pageDownloadButton.setEnabled(False)
        self.pageCancelButton.setEnabled(True)
        self.saveToButton.setEnabled(False)
        self.saveVideosToButton.setEnabled(False)
        self.adLinksBlockBrowse.setEnabled(False)
        self.adKeywordsBlockBrowse.setEnabled(False)
        self.adLinksBlockText.setReadOnly(True)
        self.adKeywordsBlockText.setReadOnly(True)

    def cancel_analysis(self):
        self.pageDownloadButton.setEnabled(True)
        self.pageCancelButton.setEnabled(False)
        self.saveToButton.setEnabled(True)
        self.saveVideosToButton.setEnabled(True)
        self.adLinksBlockBrowse.setEnabled(True)
        self.adKeywordsBlockBrowse.setEnabled(True)
        self.adLinksBlockText.setReadOnly(False)
        self.adKeywordsBlockText.setReadOnly(False)

    def start_analysis_slot(self, slot):
        self.pageDownloadButton.clicked.connect(slot)

    def cancel_slot(self, slot):
        self.pageCancelButton.clicked.connect(slot)

    def get_links(self):
        return self.adLinksBlockText.toPlainText().split('\n')

    def get_keywords(self):
        return [[token for token in tokens] for tokens in self.adKeywordsBlockText.toPlainText().split('\n')]

    def check_keywords(self):
        return "," not in self.adKeywordsBlockText.toPlainText()

    def get_save_info_path(self):
        return self.savePathLabel.text()

    def get_save_video_path(self):
        return self.chosenPathLabel.text()

    def check_size(self):
        links_lines = self.adLinksBlockText.toPlainText().split('\n')
        no_empty_lines = True
        for line in links_lines:
            if line.strip() == "":
                no_empty_lines = False
        return len(self.adLinksBlockText.toPlainText().split('\n')) \
           >= len(self.adKeywordsBlockText.toPlainText().split('\n'))\
            and no_empty_lines

    def check_texts(self):
        return self.check_keywords() and self.check_size()

    def analysis_check(self):
        if self.check_texts() and self.chosenPathLabel.text() != "":
            self.pageDownloadButton.setEnabled(True)
        else:
            self.pageDownloadButton.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
