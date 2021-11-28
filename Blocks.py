from abc import abstractmethod

from Dialogs import *


class Block:

    @abstractmethod
    def execute(self):
        pass

    @classmethod
    @abstractmethod
    def getBlockText(cls):
        pass

    @classmethod
    @abstractmethod
    def clickAction(cls, qWidget, item):
        pass


class AssignmentBlock(Block):

    def __init__(self, result, operand):
        self.result = result
        self.operand = operand

    def execute(self):
        self.result.setValue(self.operand.getValue())

    @classmethod
    def getBlockText(cls):
        return "Assign"

    @classmethod
    def clickAction(cls, qWidget, item):
        dialog = TwoInputDialog(qWidget, item, cls.getBlockText())
        dialog.exec()


class TwoOperandBlock(Block):

    def __init__(self, result, operand1, operand2):
        self.result = result
        self.operand1 = operand1
        self.operand2 = operand2

    @abstractmethod
    def execute(self):
        pass

    @classmethod
    @abstractmethod
    def getBlockText(cls):
        pass

    @classmethod
    def clickAction(cls, qWidget, item):
        dialog = ThreeInputDialog(qWidget, item, cls.getBlockText())
        dialog.exec()


class AddBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() + self.operand2.getValue())

    @classmethod
    def getBlockText(cls):
        return "Add"


class SubtractBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() - self.operand2.getValue())

    @classmethod
    def getBlockText(cls):
        return "Subtract"


class MultiplyBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() * self.operand2.getValue())

    @classmethod
    def getBlockText(cls):
        return "Multiply"


class DivideBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() / self.operand2.getValue())

    @classmethod
    def getBlockText(cls):
        return "Divide"


class ModBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() % self.operand2.getValue())

    @classmethod
    def getBlockText(cls):
        return "Mod"


def getClassFromText(text):
    return {
        AssignmentBlock.getBlockText(): AssignmentBlock,
        AddBlock.getBlockText(): AddBlock,
        SubtractBlock.getBlockText(): SubtractBlock,
        MultiplyBlock.getBlockText(): MultiplyBlock,
        DivideBlock.getBlockText(): DivideBlock,
        ModBlock.getBlockText(): ModBlock
    }.get(text.split()[0], Block)
