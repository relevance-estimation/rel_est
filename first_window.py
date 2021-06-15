import sys
from PyQt5.QtWidgets import QMainWindow,QHBoxLayout,QStackedLayout,QPushButton, QTextEdit,QVBoxLayout,QStackedWidget, QAction, QApplication,QWidget
from PyQt5.QtGui import QIcon
from app_page import Window

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.win=Window()
        self.hbox = QHBoxLayout()
        self.button = QPushButton("ret")

        self.hbox.addStretch(2)
        self.hbox.addWidget(self.win)
        self.hbox.addWidget(self.button)


        self.vbox = QVBoxLayout()
        self.vbox.addStretch(2)
        self.vbox.addLayout(self.hbox)

        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.setCentralWidget(self.widget)

        self.setWindowTitle('Main window')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())