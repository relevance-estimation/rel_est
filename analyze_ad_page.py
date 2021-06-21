#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout,
                            QPushButton, QLabel, QHBoxLayout, QSizePolicy, QLineEdit, QTextEdit, QFileDialog,
                            QMessageBox, QListWidget)
from PyQt5.QtCore import QRect, Qt, QObject, QThread, pyqtSignal, QRunnable, QThreadPool
from PyQt5.QtGui import QFont, QTextOption
from functools import partial

import video_relevance

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

        self.page = AnalyzeAdPage(self)
        self.model = video_relevance.Model()
        self.controller = AnalyzeAdPageController(self.page, self.model)
        self.setCentralWidget(self.page)

        self.show()


class AnalyzeAdPage(QWidget):
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
        self.adKeywordsBlockBrowse.clicked.connect(partial(self.read_file, self.adKeywordsBlockText))
        self.saveToButton.clicked.connect(partial(self.browse_directory, self.chosenPathLabel))

        self.adLinksBlockText.itemSelectionChanged.connect(self.analysis_check)
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
        self.analysis_check()

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
        self.adKeywordsBlockBrowse.setEnabled(False)
        self.adKeywordsBlockText.setReadOnly(True)
        self.adLinksBlockText.setEnabled(False)

    def cancel_analysis(self):
        self.pageDownloadButton.setEnabled(True)
        self.pageCancelButton.setEnabled(False)
        self.saveToButton.setEnabled(True)
        self.adLinksBlockBrowse.setEnabled(True)
        self.adKeywordsBlockBrowse.setEnabled(True)
        self.adKeywordsBlockText.setReadOnly(False)
        self.adLinksBlockText.setEnabled(True)

    def start_analysis_slot(self, slot):
        self.pageDownloadButton.clicked.connect(slot)

    def cancel_slot(self, slot):
        self.pageCancelButton.clicked.connect(slot)

    def get_paths(self):
        return [self.adLinksBlockText.item(i).text() for i in range(self.adLinksBlockText.count())]

    def get_keywords(self):
        keyword_lines = self.adKeywordsBlockText.toPlainText().split('\n')
        keywords = [[token for token in tokens] for tokens in keyword_lines]
        for i in range(len(keywords), self.adLinksBlockText.count() + 1):
            keywords.append([])
        return keywords

    def check_keywords(self):
        return "," not in self.adKeywordsBlockText.toPlainText()

    def get_save_info_path(self):
        return self.chosenPathLabel.text()

    def check_size(self):
        return self.adLinksBlockText.count() \
           >= len(self.adKeywordsBlockText.toPlainText().split('\n'))\
            and self.adLinksBlockText.count() > 0

    def check_texts(self):
        return self.check_keywords() and self.check_size()

    def analysis_check(self):
        if self.check_texts() and self.chosenPathLabel.text() != "":
            self.pageDownloadButton.setEnabled(True)
        else:
            self.pageDownloadButton.setEnabled(False)

    def show_error(self, error):
        QMessageBox.critical(self,"Ошибка", error)


class AnalyzeAdPageController:
    def __init__(self, analyze_ad_page: AnalyzeAdPage, model: video_relevance.Model):
        self.analyze_ad_page = analyze_ad_page
        self.model = model
        self.signals()

    def signals(self):
        self.analyze_ad_page.start_analysis_slot(self.start_analysis)
        self.analyze_ad_page.cancel_slot(self.cancel_analysis)

    def start_analysis(self):
        path_list = self.analyze_ad_page.get_paths()
        keywords_list = self.analyze_ad_page.get_keywords()
        save_to_path = self.analyze_ad_page.get_save_info_path()
        pool = QThreadPool.globalInstance()

        self.runnable = self.Analyzer(self.model, path_list,
                                      keywords_list, save_to_path)
        self.runnable.signal.progress.connect(self.analyze_ad_page.update_progress)
        self.runnable.signal.finished.connect(self.analyze_finished)
        self.runnable.signal.error.connect(self.error)
        pool.start(self.runnable)

    def cancel_analysis(self):
        self.runnable.kill()
        self.analyze_ad_page.cancel_analysis()
        self.analyze_ad_page.update_progress("Выполнение прервано")

    def analyze_finished(self, msg):
        self.analyze_ad_page.update_progress(msg)
        self.analyze_ad_page.cancel_analysis()
        self.analyze_ad_page.update_progress("Выполнение завершено")

    def error(self, msg):
        self.analyze_ad_page.show_error(msg)
        self.analyze_ad_page.cancel_analysis()
        self.analyze_ad_page.update_progress("Выполнение прервано")

    class Signals(QObject):
        progress = pyqtSignal(str)
        finished = pyqtSignal(str)
        error = pyqtSignal(str)

    class Analyzer(QRunnable):
        def __init__(self, model: video_relevance.Model, path_list: list,
                     keywords_list: list, save_to_path: str):
            super(AnalyzeAdPageController.Analyzer, self).__init__()
            self.model = model
            self.path_list = path_list
            self.keywords_list = keywords_list
            self.save_to_path = save_to_path
            self.total_num = len(self.path_list)

            self.is_killed = False

            self.signal = AnalyzeAdPageController.Signals()

        def update_progress(self, msg):
            self.signal.progress.emit("{}/{}: {}".format(self.cur_vid_id, self.total_num, msg))

        def run(self):
            print("started")
            for i, info in enumerate(zip(self.path_list, self.keywords_list)):
                if self.is_killed:
                    self.signal.finished.emit("Выполнение прервано")
                    return
                self.cur_vid_id = i + 1
                filename = info[0]
                name = info[0].split("/")[-1]
                keywords = info[1]
                try:
                    print(self.save_to_path + "/" + name)
                    self.model.save_ad_info(filename, self.save_to_path + "/" + name,
                                            keywords, self.update_progress)
                except Exception as e:
                    self.signal.error.emit("Ошибка обработки файла {}: ".format(filename) + str(e))
                    return
            self.signal.finished.emit("Выполнение завершено")

        def kill(self):
            self.is_killed = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())