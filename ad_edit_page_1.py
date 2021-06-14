import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel

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

        self.page = ad_edit_page_1(self)
        self.setCentralWidget(self.page)

        self.show()

class ad_edit_page_1(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Редактирование рекламы")
        self.adEditBlock = QWidget(self)
        self.adEditBlock.setGeometry(0, 0, 500, 500)
        self.adEditBlock.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.namewindow=QLabel('<h1>Редактирование ключевых слов</h1>')
        self.namefile=QLabel('Имя файла')
        self.buttonoverview = QPushButton('Обзор', self)
        self.pathEdit = QLineEdit()
        self.buttonEdit= QPushButton('Редактировать', self)

        self.buttonEdit.setMaximumWidth(100)
        self.buttonoverview.setMaximumWidth(100)

        self.buttonEdit.setEnabled(False)

        self.buttonoverview.clicked.connect(self.buttonWin1_onClick)

        grid = QGridLayout(self.adEditBlock)
        grid.setSpacing(10)

        grid.setVerticalSpacing (30)
        grid.setColumnStretch ( 0, 0 )
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        grid.addWidget(self.namewindow, 0, 0,1,3)
        grid.addWidget(self.namefile, 1, 0)
        grid.addWidget(self.pathEdit,1,1)
        grid.addWidget(self.buttonoverview, 1 , 2)
        grid.addWidget(self.buttonEdit, 2 , 2)


        if signal_state:
            self.buttonEdit.setEnabled(True)
            #if buttonEdit.clicked.connect(self.buttonWin2_onClick()):
             #   i=0
        else:
            self.buttonEdit.setEnabled(False)

        self.adEditBlock.setLayout(grid)
        self.pageVbox = QVBoxLayout(self)
        self.pageHbox = QHBoxLayout()
        self.pageHbox.addWidget(self.adEditBlock)
        self.pageVbox.addLayout(self.pageHbox)

        self.setLayout(self.pageVbox)

    def buttonWin1_onClick(self):
        #if i:
        QMessageBox.information(None, 'Сообщение от программы', "Робит")
        signal_state =True

    def buttonWin2_onClick(self):
        QMessageBox.information(None, 'Сообщение от программы', "Робит")
        signal_state = False

    def switch(self, signal_state):
        if signal_state:
            signal_state=False
        else:
            signal_state=True

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        f = open(fname, 'r')
        with f:
            data = f.read()
            self.textEdit.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
