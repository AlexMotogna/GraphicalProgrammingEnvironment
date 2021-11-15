from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget, QHBoxLayout, QListWidgetItem, QPushButton, QMessageBox
from Blocks import *


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.blockList = QListWidget()
        self.codeList = QListWidget()
        self.variableList = QListWidget()

        self.button = QPushButton('click', self)
        self.button2 = QPushButton('Add variable', self)
        self.button.clicked.connect(self.onButtonClickedShow)
        self.button2.clicked.connect(self.onClickAddVariable)

        self.codeList.setDefaultDropAction(Qt.MoveAction)

        self.blockList.setAcceptDrops(False)
        self.blockList.setDragEnabled(True)
        self.codeList.setAcceptDrops(True)
        self.codeList.setDragEnabled(True)
        self.variableList.setAcceptDrops(False)
        self.variableList.setDragEnabled(False)

        self.setGeometry(300, 350, 800, 600)

        self.myLayout = QHBoxLayout()
        self.myLayout.addWidget(self.blockList)
        self.myLayout.addWidget(self.codeList)
        self.myLayout.addWidget(self.variableList)
        self.myLayout.addWidget(self.button)
        self.myLayout.addWidget(self.button2)

        l1 = QListWidgetItem("Add")
        l2 = QListWidgetItem("Multiply")
        l3 = QListWidgetItem("Subtract")

        self.blockList.insertItem(1, l1)
        self.blockList.insertItem(2, l2)
        self.blockList.insertItem(3, l3)

        self.codeList.itemClicked.connect(self.onItemClickedCode)

        self.setWindowTitle('Drag and Drop')
        self.setLayout(self.myLayout)

        self.show()

    def onItemClickedCode(self, item):
        getClassFromText(item.text()).clickAction(self, item)

    def onItemClickedVariable(self, item):
        pass

    def onButtonClickedShow(self):
        alert = QMessageBox()
        text = ''

        for i in range(self.codeList.count()):
            text += self.codeList.item(i).text()
            text += ' '

        alert.setText(text)
        alert.exec()

    def onClickAddVariable(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
        if ok and text:
            self.variableList.addItem(QListWidgetItem(text))
