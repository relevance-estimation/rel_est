import sys

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
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
        self.adEditBlock.setGeometry(0, 0, 840, 680)

        #self.adEditBlock.setMaximumSize(500, 250)



        grid = QGridLayout()


        self.table = QTableWidget(self)
        self.table.setGeometry(0,0,700,405)
        self.table.setColumnCount(4)
        self.table.setRowCount(10)

        self.table.setHorizontalHeaderLabels(["Путь к файлу", "Фрагмент", "Тип релевантности", "Оценка релевантности"])

        for i in range(3): self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)


        self.buttonReturn = QPushButton('Возврат', self)
        grid.addWidget(self.buttonReturn, 1, 10)

        self.table.resizeColumnsToContents()
        grid.addWidget(self.table, 0, 0, 1, 11 )
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

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
