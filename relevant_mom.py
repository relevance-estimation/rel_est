import sys

from PyQt5.QtWidgets import  QDesktopWidget, QApplication, QLabel, QFileDialog,\
    QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,\
    QTableWidgetItem

from PyQt5.QtCore import QRect, Qt, QAbstractTableModel

from functools import partial

from relevant_moment import RelevantMoment
from relevant_moment_result import RelevantMomentResult

import pandas as pd

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

        self.page = AdEditPage(self)
        self.setCentralWidget(self.page)

        self.show()


class AdEditPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.UiComponents()
        self.signals()

    def UiComponents(self):
        self.layout = QVBoxLayout(self)

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

        #self.tab1.buttonEdit.clicked.connect(self.launch_success)
        #df = pd.DataFrame(data=[[1,2,3,4,5]])
        #self.load_data(df)

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
        return self.tab1.nameInfoRec.text()

    def get_vid_info_path(self):
        return self.tab1.nameInfoVid.text()

    def get_ad_path(self):
        return self.tab1.nameRec.text()

    def get_vid_path(self):
        return self.tab1.nameVid.text()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
