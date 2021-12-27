from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget, QHBoxLayout, QListWidgetItem
from CodeRunner import *


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.blockList = QListWidget()
        self.blockList.setAcceptDrops(False)
        self.blockList.setDragEnabled(True)

        self.codeList = QListWidget()
        self.codeList.setDefaultDropAction(Qt.MoveAction)
        self.codeList.setAcceptDrops(True)
        self.codeList.setDragEnabled(True)

        self.variableList = QListWidget()
        self.variableList.setAcceptDrops(False)
        self.variableList.setDragEnabled(False)

        self.executeButton = QPushButton('Execute', self)
        self.addVariableButton = QPushButton('Add variable', self)
        self.executeButton.clicked.connect(self.onExecuteButtonClicked)
        self.addVariableButton.clicked.connect(self.onClickAddVariable)

        self.blockLabel = QLabel("Blocks")
        self.codeLabel = QLabel("Code")
        self.variableLabel = QLabel("Variables")

        self.setGeometry(400, 100, 1250, 800)
        self.myLayout = QHBoxLayout()

        self.blockLayout = QVBoxLayout()
        self.blockLayout.addWidget(self.blockLabel)
        self.blockLayout.addWidget(self.blockList)

        self.codeLayout = QVBoxLayout()
        self.codeLayout.addWidget(self.codeLabel)
        self.codeLayout.addWidget(self.codeList)

        self.variableLayout = QVBoxLayout()
        self.variableLayout.addWidget(self.variableLabel)
        self.variableLayout.addWidget(self.variableList)

        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.addWidget(self.addVariableButton)
        self.buttonLayout.addWidget(self.executeButton)

        self.myLayout.addLayout(self.blockLayout)
        self.myLayout.addLayout(self.codeLayout)
        self.myLayout.addLayout(self.variableLayout)
        self.myLayout.addLayout(self.buttonLayout)

        l1 = QListWidgetItem(AddBlock.getBlockText() + " ...")
        l2 = QListWidgetItem(MultiplyBlock.getBlockText() + " ...")
        l3 = QListWidgetItem(SubtractBlock.getBlockText() + " ...")
        l4 = QListWidgetItem(DivideBlock.getBlockText() + " ...")
        l5 = QListWidgetItem(ModBlock.getBlockText() + " ...")
        l6 = QListWidgetItem(AssignmentBlock.getBlockText() + " ...")
        l7 = QListWidgetItem(PrintBlock.getBlockText() + " ...")
        l8 = QListWidgetItem(IfBlock.getBlockText() + " ...")
        l9 = QListWidgetItem(EndIfBlock.getBlockText())
        l10 = QListWidgetItem(WhileBlock.getBlockText() + " ...")
        l11 = QListWidgetItem(EndWhileBlock.getBlockText())

        self.blockList.insertItem(1, l1)
        self.blockList.insertItem(2, l2)
        self.blockList.insertItem(3, l3)
        self.blockList.insertItem(4, l4)
        self.blockList.insertItem(5, l5)
        self.blockList.insertItem(6, l6)
        self.blockList.insertItem(7, l7)
        self.blockList.insertItem(8, l8)
        self.blockList.insertItem(9, l9)
        self.blockList.insertItem(10, l10)
        self.blockList.insertItem(11, l11)

        self.codeList.itemClicked.connect(self.onItemClickedCode)
        self.variableList.itemClicked.connect(self.onItemClickedVariable)

        self.setWindowTitle('Graphical Programming Environment')
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
            alertError(str(e))

    def variableInList(self, variableName):
        for i in range(self.variableList.count()):
            if self.variableList.item(i).text() == variableName:
                return True
        return False

    def isVariableNameValid(self, variableName):
        return not(self.variableInList(variableName)
                   or variableName.__contains__("...")
                   or variableName == "instrIndex"
                   or variableName == "printLog")\
               and variableName[0].isalpha()

    def onClickAddVariable(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter variable name:')
        if ok and text:
            if self.isVariableNameValid(text):
                self.variableList.addItem(QListWidgetItem(text))
            else:
                alertError("Invalid variable name")
