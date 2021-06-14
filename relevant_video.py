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

        self.buttonEdit.setEnabled(False)

        self.buttonVid.clicked.connect(self.buttonWin1_onClick)
        self.buttonRec.clicked.connect(self.buttonWin2_onClick)


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

    def buttonWin1_onClick(self):
        select_file = getOpenFilesAndDirs()
        if select_file:
            self.pathVid.clear()
            self.pathVid.addItems(select_file)
            self.buttonEdit.setEnabled(True)
        else:
            msg = QtWidgets.QMessageBox.information(self, 'Message', 'Вы ничего не выбрали.')

    def buttonWin2_onClick(self):
        select_file = getOpenFilesAndDirs()
        if select_file:
            self.pathRec.clear()
            self.pathRec.addItems(select_file)
            self.buttonEdit.setEnabled(True)
        else:
            msg = QtWidgets.QMessageBox.information(self, 'Message', 'Вы ничего не выбрали.')





def getOpenFilesAndDirs(parent=None, caption='', directory='',
                        filter='', initialFilter='', options=None):
    def updateText():
        # обновить содержимое виджета редактирования строки выбранными файлами
        selected = []
        for index in view.selectionModel().selectedRows():
            selected.append('"{}"'.format(index.data()))
        pathEdit.setText(' '.join(selected))

    dialog = QtWidgets.QFileDialog(parent, windowTitle=caption)
    dialog.setFileMode(dialog.ExistingFiles)
    if options:
        dialog.setOptions(options)
    dialog.setOption(dialog.DontUseNativeDialog, True)  # !!!
    if directory:
        dialog.setDirectory(directory)
    if filter:
        dialog.setNameFilter(filter)
        if initialFilter:
            dialog.selectNameFilter(initialFilter)

    # по умолчанию, если каталог открыт в режиме списка файлов,
    # QFileDialog.accept() показывает содержимое этого каталога,
    # но нам нужно иметь возможность "открывать" и каталоги, как мы можем делать с файлами,
    # поэтому мы просто переопределяем `accept()` с реализацией QDialog по умолчанию,
    # которая просто вернет `dialog.selectedFiles()`

    dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)

    # в неродном диалоге есть много представлений элементов,
    # но те, которые отображают фактическое содержимое, создаются внутри QStackedWidget;
    # это QTreeView и QListView, и дерево используется только тогда,
    # когда viewMode установлен на QFileDialog.Details, что не в этом случае.

    stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
    view = stackedWidget.findChild(QtWidgets.QListView)
    view.selectionModel().selectionChanged.connect(updateText)

    pathEdit = dialog.findChild(QtWidgets.QLineEdit)
    # очищаем содержимое строки редактирования всякий раз, когда изменяется текущий каталог
    dialog.directoryEntered.connect(lambda: pathEdit.setText(''))

    dialog.exec_()
    return dialog.selectedFiles()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
