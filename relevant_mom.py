import sys

from PyQt5.QtWidgets import  QDesktopWidget, QApplication, QLabel, QFileDialog,\
    QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout

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

    def UiComponents(self):
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = RelevantMoment(self.tabs)
        self.tab2 = RelevantMomentResult(self.tabs)


        # Add tabs
        self.tabs.addTab(self.tab1, "Выбор")
        self.tabs.addTab(self.tab2, "Результат")
        self.tabs.setTabEnabled(1, False)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.tab1.buttonEdit.clicked.connect(self.editResult)

    def editResult(self):
        self.tabs.setTabEnabled(1, True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
