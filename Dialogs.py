from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox


class PrintInputDialog(QDialog):

    def __init__(self, qWidget, item):
        super().__init__()

        self.qWidget = qWidget
        self.item = item

        self.setGeometry(300, 350, 400, 400)
        self.layout = QVBoxLayout()
        self.setWindowTitle("Input")
        self.setLayout(self.layout)

        self.labelVariable = QLabel("Variable to be printed")
        self.textboxVariable = QLineEdit(self)
        self.finishButton = QPushButton("Confirm", self)
        self.deleteButton = QPushButton("Delete", self)

        self.finishButton.clicked.connect(self.onConfirmButtonPressed)
        self.deleteButton.clicked.connect(self.onDeleteButtonPressed)

        self.layout.addWidget(self.labelVariable)
        self.layout.addWidget(self.textboxVariable)
        self.layout.addWidget(self.finishButton)
        self.layout.addWidget(self.deleteButton)

    def onDeleteButtonPressed(self):
        reply = QMessageBox.question(self, 'Delete', 'Are you sure you want to delete this item?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.qWidget.codeList.takeItem(self.qWidget.codeList.row(self.item))
            self.accept()

    def onConfirmButtonPressed(self):
        try:
            verifyResultVariable(self.qWidget, self.textboxVariable.text(), "Invalid variable")

            self.item.setText("Print " + self.textboxVariable.text())
            self.accept()

        except ValueError as e:
            alert = QMessageBox()
            alert.setText(str(e))
            alert.exec()


class TwoInputDialog(QDialog):

    def __init__(self, qWidget, item, opString):
        super().__init__()

        self.opString = opString
        self.item = item
        self.qWidget = qWidget

        self.setGeometry(300, 350, 400, 400)
        self.layout = QVBoxLayout()
        self.setWindowTitle("Input")
        self.setLayout(self.layout)

        self.labelResult = QLabel("Assigned variable")
        self.textboxResult = QLineEdit(self)
        self.labelOperand1 = QLabel("Assignment Operand")
        self.textboxOperand1 = QLineEdit(self)
        self.finishButton = QPushButton("Confirm", self)
        self.deleteButton = QPushButton("Delete", self)

        self.finishButton.clicked.connect(self.onConfirmButtonPressed)
        self.deleteButton.clicked.connect(self.onDeleteButtonPressed)

        self.layout.addWidget(self.labelResult)
        self.layout.addWidget(self.textboxResult)
        self.layout.addWidget(self.labelOperand1)
        self.layout.addWidget(self.textboxOperand1)
        self.layout.addWidget(self.finishButton)
        self.layout.addWidget(self.deleteButton)

    def onDeleteButtonPressed(self):
        reply = QMessageBox.question(self, 'Delete', 'Are you sure you want to delete this item?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.qWidget.codeList.takeItem(self.qWidget.codeList.row(self.item))
            self.accept()

    def onConfirmButtonPressed(self):
        try:
            verifyResultVariable(self.qWidget, self.textboxResult.text(), "Invalid assigned variable")
            verifyOperand(self.qWidget, self.textboxOperand1.text(), "Invalid operand")

            self.item.setText(self.opString + " " +
                              self.textboxResult.text() + " " +
                              self.textboxOperand1.text())
            self.accept()

        except ValueError as e:
            alert = QMessageBox()
            alert.setText(str(e))
            alert.exec()


class ThreeInputDialog(TwoInputDialog):

    def __init__(self, qWidget, item, opString):
        super().__init__(qWidget, item, opString)

        self.labelOperand2 = QLabel("Second Operand")
        self.textboxOperand2 = QLineEdit(self)

        self.layout.removeWidget(self.finishButton)
        self.layout.removeWidget(self.deleteButton)
        self.layout.addWidget(self.labelOperand2)
        self.layout.addWidget(self.textboxOperand2)
        self.layout.addWidget(self.finishButton)
        self.layout.addWidget(self.deleteButton)

    def onConfirmButtonPressed(self):
        try:
            verifyResultVariable(self.qWidget, self.textboxResult.text(), "Invalid result variable")
            verifyOperand(self.qWidget, self.textboxOperand1.text(), "Invalid first operand")
            verifyOperand(self.qWidget, self.textboxOperand2.text(), "Invalid second operand ")

            self.item.setText(self.opString + " " +
                              self.textboxResult.text() + " " +
                              self.textboxOperand1.text() + " " +
                              self.textboxOperand2.text())
            self.accept()

        except ValueError as e:
            alert = QMessageBox()
            alert.setText(str(e))
            alert.exec()


def verifyResultVariable(qWidget, variableText, errorText):
    if not qWidget.variableInList(variableText):
        raise ValueError(errorText)


def verifyOperand(qWidget, valueText, errorText):
    if not (qWidget.variableInList(valueText) or valueText.isnumeric()):
        raise ValueError(errorText)
