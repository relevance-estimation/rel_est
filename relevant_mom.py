import sys

from PyQt5.QtWidgets import  QDesktopWidget, QApplication, QLabel, QFileDialog,\
    QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout

from functools import partial

from relevant_moment import RelevantMoment
from relevant_moment_result import RelevantMomentResult


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

    def browse_and_check(self, browseLabel):
        self.browse_file(browseLabel)
        if self.tab1.pathInfoVid.text() != "" and self.tab1.pathInfoRec.text() != "" \
            and self.tab1.pathVid.text() != "" and self.tab1.pathRec.text() != "":
            self.tab1.buttonEdit.setEnabled(True)

    def browse_file(self, browseLabel):
        select_file = QFileDialog.getOpenFileName(self)
        if select_file[0] != "":
            browseLabel.clear()
            browseLabel.insert(select_file[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
