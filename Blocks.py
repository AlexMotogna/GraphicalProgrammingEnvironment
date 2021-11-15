from abc import abstractmethod

from PyQt5 import QtWidgets


class Block:

    @abstractmethod
    def execute(self):
        pass

    @staticmethod
    @abstractmethod
    def clickAction(qWidget, item):
        pass


class AssignmentBlock(Block):

    def __init__(self, result, operand):
        self.result = result
        self.operand = operand

    def execute(self):
        self.result.setValue(self.operand.getValue())

    @staticmethod
    def clickAction(qWidget, item):
        pass


class TwoOperandBlock(Block):

    def __init__(self, result, operand1, operand2):
        self.result = result
        self.operand1 = operand1
        self.operand2 = operand2

    @abstractmethod
    def execute(self):
        pass

    @staticmethod
    @abstractmethod
    def clickAction(qWidget, item):
        pass


class AddBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() + self.operand2.getValue())

    @staticmethod
    def clickAction(qWidget, item):
        text, ok = QtWidgets.QInputDialog.getText(qWidget, 'Input Dialog', 'Enter text:')
        if ok and text:
            item.setText("Add " + text)


class SubtractBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() - self.operand2.getValue())

    @staticmethod
    def clickAction(qWidget, item):
        pass


class MultiplyBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() * self.operand2.getValue())

    @staticmethod
    def clickAction(qWidget, item):
        pass


class DivideBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() / self.operand2.getValue())

    @staticmethod
    def clickAction(qWidget, item):
        pass


class ModBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() % self.operand2.getValue())

    @staticmethod
    def clickAction(qWidget, item):
        pass


def getClassFromText(text):
    return {
        "Assign": AssignmentBlock,
        "Add": AddBlock,
        "Subtract": SubtractBlock,
        "Multiply": MultiplyBlock,
        "Divide": DivideBlock,
        "Mod": ModBlock
    }.get(text.split()[0], Block)
