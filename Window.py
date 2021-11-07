from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget, QHBoxLayout, QListWidgetItem, QPushButton, QMessageBox


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.myListWidget1 = QListWidget()
        self.myListWidget2 = QListWidget()

        self.button = QPushButton('click', self)
        self.button.clicked.connect(self.onButtonClickedShow)

        self.myListWidget2.setDefaultDropAction(Qt.MoveAction)

        self.myListWidget1.setAcceptDrops(False)
        self.myListWidget1.setDragEnabled(True)
        self.myListWidget2.setAcceptDrops(True)
        self.myListWidget2.setDragEnabled(True)

        self.setGeometry(300, 350, 800, 600)

        self.myLayout = QHBoxLayout()
        self.myLayout.addWidget(self.myListWidget1)
        self.myLayout.addWidget(self.myListWidget2)
        self.myLayout.addWidget(self.button)

        l1 = QListWidgetItem("Add")
        l2 = QListWidgetItem("Multiply")
        l3 = QListWidgetItem("if (<your text>)")

        self.myListWidget1.insertItem(1, l1)
        self.myListWidget1.insertItem(2, l2)
        self.myListWidget1.insertItem(3, l3)

        self.myListWidget1.itemEntered.connect(self.onItemEnteredDelete)
        self.myListWidget2.itemClicked.connect(self.onItemClicked)

        self.setWindowTitle('Drag and Drop')
        self.setLayout(self.myLayout)

        self.show()

    def onItemClicked(self, item):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
        if ok:
            item.setText(text)

    def onItemEnteredDelete(self, item):
        self.myListWidget1.removeItemWidget(item)

    def onButtonClickedShow(self):
        alert = QMessageBox()
        text = ''

        for i in range(self.myListWidget2.count()):
            text += self.myListWidget2.item(i).text()
            text += ' '

        alert.setText(text)
        alert.exec()

    def removeItem(self, item):
        self.myListWidget2.removeItemWidget(item)
