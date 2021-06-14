import sys

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,\
    QFileDialog,QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget,\
    QTableWidgetItem,QApplication,QWidget,QHeaderView


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

        self.page = RelevantMomentResult(self)
        self.setCentralWidget(self.page)

        self.show()

class RelevantMomentResult(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Редактирование рекламы")
        self.adEditBlock = QWidget(self)
        self.adEditBlock.setGeometry(0, 0, 500, 500)


        #self.adEditBlock.setMaximumSize(500, 250)

        self.namewindow=QLabel('<h1>Релевантные моменты</h1>')
        self.namewindow.setAlignment(Qt.AlignCenter)
        self.pathInfoVid = QLineEdit()
        self.namefile=QLabel('Имя файла: ')


        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setVerticalSpacing(30)

        self.table = QTableWidget(self)
        self.table.setGeometry(0,0,700,405)
        self.table.setColumnCount(4)
        self.table.setRowCount(10)

        self.table.setHorizontalHeaderLabels(["Путь к файлу", "Фрагмент", "Тип релевантности", "Оценка релевантности"])

        for i in range(3): self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)


        self.buttonReturn = QPushButton('Возврат', self)
        grid.addWidget(self.buttonReturn, 3, 10)


        grid.addWidget(self.namewindow, 0,1,1,10)
        grid.addWidget(self.namefile, 1,1)
        grid.addWidget(self.pathInfoVid, 1,2,1,9)

        self.pathInfoVid.setMaximumWidth(500)

        self.table.resizeColumnsToContents()
        grid.addWidget(self.table, 2, 1, 1, 10 )

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #self.table.verticalHeader().setStretchLastSection(True)
        #self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.table.showGrid()
        #self.vertical = self.table.horizontalHeader().resizeRowsToContents(QtGui.QHeaderView.stretchLastSection)



        #self.vertical = self.table.

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
