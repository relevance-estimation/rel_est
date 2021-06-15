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

        self.page = RelevantVideo(self)
        self.setCentralWidget(self.page)

        self.show()

class RelevantVideo(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Релевантное видео")
        self.adEditBlock = QWidget(self)
        self.adEditBlock.setGeometry(0, 0, 500, 500)
        self.adEditBlock.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        #self.adEditBlock.setMaximumSize(500, 250)


        self.namewindow=QLabel('<h1>Релевантные видео</h1>')
        self.namewindow.setAlignment(Qt.AlignCenter)

        #self.namewindow.setFixedHeight()


        self.nameVid=QLabel('Набор видео')
        self.nameRec=QLabel('Набор реклам')

        self.buttonVid = QPushButton('Обзор', self)
        self.buttonRec = QPushButton('Обзор', self)

        self.pathVid = QListWidget()
        self.pathRec = QListWidget()

        self.buttonEdit= QPushButton('Анализ', self)



        #self.buttonEdit.setMaximumWidth(100)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.setVerticalSpacing (30)

        grid.addWidget(self.namewindow, 0, 0,1,4)

        grid.addWidget(self.nameVid, 1, 0)
        grid.addWidget(self.nameRec, 3, 0)


        grid.addWidget(self.pathVid,1,1,2,1)
        grid.addWidget(self.pathRec,3,1,2,1)


        grid.addWidget(self.buttonVid, 1 , 2)
        grid.addWidget(self.buttonRec, 3 , 2)



        grid.addWidget(self.buttonEdit, 5 , 2)


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
