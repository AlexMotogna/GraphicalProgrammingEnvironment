from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox


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

    def verifyResultVariable(self, variableText, errorText):
        if not self.qWidget.variableInList(variableText):
            raise ValueError(errorText)

    def verifyOperand(self, valueText, errorText):
        if not (self.qWidget.variableInList(valueText) or valueText.isnumeric()):
            raise ValueError(errorText)

    def onDeleteButtonPressed(self):
        reply = QMessageBox.question(self, 'Delete', 'Are you sure you want to delete this item?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.qWidget.codeList.takeItem(self.qWidget.codeList.row(self.item))
            self.accept()

    def onConfirmButtonPressed(self):
        try:
            self.verifyResultVariable(self.textboxResult.text(), "Invalid assigned variable")
            self.verifyOperand(self.textboxOperand1.text(), "Invalid operand")

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
            super().verifyResultVariable(self.textboxResult.text(), "Invalid result variable")
            super().verifyOperand(self.textboxOperand1.text(), "Invalid first operand")
            super().verifyOperand(self.textboxOperand2.text(), "Invalid second operand ")

            self.item.setText(self.opString + " " +
                              self.textboxResult.text() + " " +
                              self.textboxOperand1.text() + " " +
                              self.textboxOperand2.text())
            self.accept()

        except ValueError as e:
            alert = QMessageBox()
            alert.setText(str(e))
            alert.exec()
