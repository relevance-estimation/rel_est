import sys

from PyQt5.QtWidgets import  QDesktopWidget, QApplication, QLabel, QFileDialog,\
    QMainWindow, QApplication,QMessageBox, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,\
    QTableWidgetItem

from PyQt5.QtCore import QRect, Qt, QAbstractTableModel

from functools import partial

from relevant_moment import RelevantMoment
from relevant_moment_result import RelevantMomentResult
import pickle

import pandas as pd
import video_relevance

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

        self.page = RelevantMoments(self)
        self.model = video_relevance.Model()

        self.page_controller = RelevantMomentsController(self.page, self.model)

        self.setCentralWidget(self.page)

        self.show()


class RelevantMoments(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.setWindowTitle("Релевантные моменты")

    def initUI(self):
        self.UiComponents()
        self.signals()

    def UiComponents(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = RelevantMoment(self.tabs)
        self.tab2 = RelevantMomentResult(self.tabs)


        # Add tabs
        self.tabs.addTab(self.tab1, "Выбор")
        self.tabs.addTab(self.tab2, "Результат")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def signals(self):
        self.tabs.setTabEnabled(1, False)

        self.tab1.pathInfoVid.setReadOnly(True)
        self.tab1.pathInfoRec.setReadOnly(True)
        self.tab1.pathVid.setReadOnly(True)
        self.tab1.pathRec.setReadOnly(True)

        self.tab1.buttonEdit.setEnabled(False)

        self.tab1.buttonInfoVid.clicked.connect(partial(self.browse_and_check, self.tab1.pathInfoVid))
        self.tab1.buttonInfoRec.clicked.connect(partial(self.browse_and_check, self.tab1.pathInfoRec))
        self.tab1.buttonVid.clicked.connect(partial(self.browse_and_check, self.tab1.pathVid))
        self.tab1.buttonRec.clicked.connect(partial(self.browse_and_check, self.tab1.pathRec))

        df = pd.DataFrame(data=[[1,2,3,4,5]])
        self.load_data(df)

    def browse_and_check(self, browseLabel):
        self.browse_file(browseLabel)
        if self.tab1.pathInfoVid.text() != "" and self.tab1.pathInfoRec.text() != "":
            #and self.tab1.pathVid.text() != "" and self.tab1.pathRec.text() != "":
            self.tab1.buttonEdit.setEnabled(True)

    def browse_file(self, browseLabel):
        select_file = QFileDialog.getOpenFileName(self)
        if select_file[0] != "":
            browseLabel.clear()
            browseLabel.insert(select_file[0])

    def load_data(self, df):
        df.columns = ["Фрагмент", "Тип релевантности", "Общая оценка", "Текст", "Цвета"]
        self.tab2.table.setModel(PandasModel(df))

    def launch_success(self):
        self.tabs.setTabEnabled(1, True)
        self.tabs.setCurrentIndex(1)
        self.tab2.pathInfoVid.setText(self.tab1.pathInfoRec.text())
        self.tab1.buttonEdit.setEnabled(False)

    def start_analysis_slot(self, slot):
        self.tab1.buttonEdit.clicked.connect(slot)

    def get_ad_info_path(self):
        return self.tab1.pathInfoRec.text()

    def get_vid_info_path(self):
        return self.tab1.pathInfoVid.text()

    def get_ad_path(self):
        return self.tab1.pathRec.text()

    def get_vid_path(self):
        return self.tab1.pathVid.text()

    def show_error(self, error):
        QMessageBox.critical(self,"Ошибка", error)

    def launch_fail(self):
        self.tab1.buttonEdit.setEnabled(False)

class RelevantMomentsController():
    def __init__(self, relevant_moments_page, model):
        self.relevant_moments_page = relevant_moments_page
        self.signals()
        self.model = model

    def signals(self):
        self.relevant_moments_page.start_analysis_slot(self.analyze)

    def analyze(self):
        ad_info = self.check_file(self.relevant_moments_page.get_ad_info_path())
        if ad_info == False:
            return
        vid_infos = self.check_file(self.relevant_moments_page.get_vid_info_path())
        if vid_infos == False:
            return
        try:
            estimate = self.model.get_estimate(ad_info, vid_infos, ['' for video in vid_infos])
        except:
            self.relevant_moments_page.show_error("Ошибка анализа файла")
            self.relevant_moments_page.launch_fail()
            return
        df = pd.DataFrame(data=estimate[0], header=False)
        df = df.iloc[:, 1:]
        self.relevant_moments_page.load_data(df)
        self.relevant_moments_page.launch_success()

    def check_file(self, path):
        print("path:", path)
        try:
            with open(path, "rb") as f:
                f.seek(0)
                vids = pickle.load(f)
            return vids.videos
        except:
            self.relevant_moments_page.show_error("Ошибка при чтении файла")
            self.relevant_moments_page.launch_fail()
            return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
