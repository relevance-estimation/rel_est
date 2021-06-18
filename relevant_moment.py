import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QFileDialog

signal_state = False


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

        self.page = RelevantMoment(self)
        self.setCentralWidget(self.page)

        self.show()

class RelevantMoment(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Редактирование рекламы")
        self.adEditBlock = QWidget(self)
        self.adEditBlock.setGeometry(0, 0, 500, 500)
        self.adEditBlock.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        #self.adEditBlock.setMaximumSize(500, 250)


        self.namewindow=QLabel('<h1>Релевантные моменты</h1>')
        self.namewindow.setAlignment(Qt.AlignCenter)

        #self.namewindow.setFixedHeight()

        self.nameInfoVid=QLabel('Инфо-видео')
        self.nameInfoRec=QLabel('Инфо-видео')
        self.nameVid=QLabel('Видео')
        self.nameRec=QLabel('Реклама')

        self.buttonInfoVid = QPushButton('Обзор', self)
        self.buttonInfoRec = QPushButton('Обзор', self)

        self.pathInfoVid = QLineEdit()
        self.pathInfoRec = QLineEdit()

        self.buttonEdit= QPushButton('Запуск', self)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.setVerticalSpacing (30)
        grid.setColumnStretch ( 0, 0 )
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        grid.addWidget(self.namewindow, 0, 0,1,4)

        grid.addWidget(self.nameInfoVid, 1, 0)
        grid.addWidget(self.nameInfoRec, 2, 0)

        grid.addWidget(self.pathInfoVid,1,1)
        grid.addWidget(self.pathInfoRec,2,1)

        grid.addWidget(self.buttonInfoVid, 1 , 2)
        grid.addWidget(self.buttonInfoRec, 2 , 2)


        grid.addWidget(self.buttonEdit, 3 , 2)


        self.adEditBlock.setLayout(grid)
        self.pageVbox = QVBoxLayout(self)
        self.pageHbox = QHBoxLayout()
        self.pageHbox.addWidget(self.adEditBlock)
        self.pageVbox.addLayout(self.pageHbox)

        self.setLayout(self.pageVbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
