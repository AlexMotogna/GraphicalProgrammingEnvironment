from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget, QHBoxLayout, QListWidgetItem
from Blocks import *
from CodeRunner import *
from Variable import Variable


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.blockList = QListWidget()
        self.codeList = QListWidget()
        self.variableList = QListWidget()

        self.executeButton = QPushButton('Execute', self)
        self.addVariableButton = QPushButton('Add variable', self)
        self.executeButton.clicked.connect(self.onExecuteButtonClicked)
        self.addVariableButton.clicked.connect(self.onClickAddVariable)

        self.codeList.setDefaultDropAction(Qt.MoveAction)

        self.blockList.setAcceptDrops(False)
        self.blockList.setDragEnabled(True)
        self.codeList.setAcceptDrops(True)
        self.codeList.setDragEnabled(True)
        self.variableList.setAcceptDrops(False)
        self.variableList.setDragEnabled(False)

        self.setGeometry(400, 100, 1250, 800)

        self.myLayout = QHBoxLayout()
        self.myLayout.addWidget(self.blockList)
        self.myLayout.addWidget(self.codeList)
        self.myLayout.addWidget(self.variableList)
        self.myLayout.addWidget(self.addVariableButton)
        self.myLayout.addWidget(self.executeButton)

        l1 = QListWidgetItem(AddBlock.getBlockText() + " ...")
        l2 = QListWidgetItem(MultiplyBlock.getBlockText() + " ...")
        l3 = QListWidgetItem(SubtractBlock.getBlockText() + " ...")
        l4 = QListWidgetItem(DivideBlock.getBlockText() + " ...")
        l5 = QListWidgetItem(ModBlock.getBlockText() + " ...")
        l6 = QListWidgetItem(AssignmentBlock.getBlockText() + " ...")
        l7 = QListWidgetItem(PrintBlock.getBlockText() + " ...")

        self.blockList.insertItem(1, l1)
        self.blockList.insertItem(2, l2)
        self.blockList.insertItem(3, l3)
        self.blockList.insertItem(4, l4)
        self.blockList.insertItem(5, l5)
        self.blockList.insertItem(6, l6)
        self.blockList.insertItem(7, l7)

        self.codeList.itemClicked.connect(self.onItemClickedCode)
        self.variableList.itemClicked.connect(self.onItemClickedVariable)

        self.setWindowTitle('Drag and Drop')
        self.setLayout(self.myLayout)

        self.show()

    def onItemClickedCode(self, item):
        getClassFromText(item.text()).clickAction(self, item)

    def onItemClickedVariable(self, item):
        reply = QMessageBox.question(self, 'Delete', 'Do you want to delete this item',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.variableList.takeItem(self.variableList.row(item))

    def onExecuteButtonClicked(self):
        codeStringList = []
        for index in range(self.codeList.count()):
            codeStringList.append(self.codeList.item(index).text())
        variables = []
        for index in range(self.variableList.count()):
            variables.append(Variable(0, self.variableList.item(index).text()))

        try:
            runCode(codeStringList, variables)
        except ValueError as e:
            alert = QMessageBox()
            alert.setText(str(e))
            alert.exec()

    def variableInList(self, variableName):
        for i in range(self.variableList.count()):
            if self.variableList.item(i).text() == variableName:
                return True
        return False

    def isVariableNameValid(self, variableName):
        return not(self.variableInList(variableName)
                   or variableName.__contains__("...")
                   or variableName == "instrIndex")\
               and variableName[0].isalpha()

    def onClickAddVariable(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter variable name:')
        if ok and text:
            if self.isVariableNameValid(text):
                self.variableList.addItem(QListWidgetItem(text))
            else:
                alert = QMessageBox()
                alert.setText("Invalid variable name")
                alert.exec()
