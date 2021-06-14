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

        self.page = AdEditPage1(self)
        self.setCentralWidget(self.page)

        self.show()

class AdEditPage1(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Редактирование рекламы")
        self.adEditBlock = QWidget(self)

        self.adEditBlock.setMaximumSize(500, 250)

        self.namewindow=QLabel('<h1>Редактирование ключевых слов</h1>')
        self.namewindow.setAlignment(Qt.AlignCenter)
        self.namefile=QLabel('Имя файла')
        self.buttonoverview = QPushButton('Обзор', self)
        self.pathEdit = QLineEdit()
        self.buttonEdit= QPushButton('Редактировать', self)

        self.pathEdit.setReadOnly(True)

        self.buttonEdit.setMaximumWidth(100)
        self.buttonoverview.setMaximumWidth(100)

        self.buttonEdit.setEnabled(False)

        self.buttonoverview.clicked.connect(self.buttonWin1_onClick)

        grid = QGridLayout()
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



        self.adEditBlock.setLayout(grid)
        self.pageVbox = QVBoxLayout(self)
        self.pageHbox = QHBoxLayout()
        self.pageHbox.addWidget(self.adEditBlock)
        self.pageVbox.addLayout(self.pageHbox)

        self.setLayout(self.pageVbox)

    def buttonWin1_onClick(self):
        select_file = getOpenFilesAndDirs()
        if select_file:
            self.pathEdit.clear()
            self.pathEdit.insert(select_file[0])
            self.buttonEdit.setEnabled(True)
        else:
            msg = QtWidgets.QMessageBox.information(self, 'Message', 'Вы ничего не выбрали.')

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
