from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget, QHBoxLayout, QListWidgetItem, QMessageBox
from Blocks import *


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.blockList = QListWidget()
        self.codeList = QListWidget()
        self.variableList = QListWidget()

        self.showButton = QPushButton('click', self)
        self.addVariableButton = QPushButton('Add variable', self)
        self.showButton.clicked.connect(self.onButtonClickedShow)
        self.addVariableButton.clicked.connect(self.onClickAddVariable)

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
        self.myLayout.addWidget(self.showButton)
        self.myLayout.addWidget(self.addVariableButton)

        l1 = QListWidgetItem(AddBlock.getBlockText() + " ...")
        l2 = QListWidgetItem(MultiplyBlock.getBlockText() + " ...")
        l3 = QListWidgetItem(SubtractBlock.getBlockText() + " ...")
        l4 = QListWidgetItem(DivideBlock.getBlockText() + " ...")
        l5 = QListWidgetItem(ModBlock.getBlockText() + " ...")
        l6 = QListWidgetItem(AssignmentBlock.getBlockText() + " ...")

        self.blockList.insertItem(1, l1)
        self.blockList.insertItem(2, l2)
        self.blockList.insertItem(3, l3)
        self.blockList.insertItem(4, l4)
        self.blockList.insertItem(5, l5)
        self.blockList.insertItem(6, l6)

        self.codeList.itemClicked.connect(self.onItemClickedCode)
        self.variableList.itemClicked.connect(self.onClickAddVariable)

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
            text += ', '

        alert.setText(text)
        alert.exec()

    def variableInList(self, variableName):
        for i in range(self.variableList.count()):
            if self.variableList.item(i).text() == variableName:
                return True
        return False

    def onClickAddVariable(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
        if ok and text and not self.variableInList(text):
            self.variableList.addItem(QListWidgetItem(text))
