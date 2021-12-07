from abc import abstractmethod

from Dialogs import *
from Variable import Constant


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

    @classmethod
    @abstractmethod
    def factoryMethod(cls, codeString, variableList):
        pass


class PrintBlock(Block):

    def __init__(self, variable):
        self.variable = variable

    def execute(self):
        print(self.variable.getValue())

    @classmethod
    def getBlockText(cls):
        return "Print"

    @classmethod
    def clickAction(cls, qWidget, item):
        dialog = PrintInputDialog(qWidget, item)
        dialog.exec()

    @classmethod
    @abstractmethod
    def factoryMethod(cls, codeString, variableList):
        codeStringSplit = codeString.split()

        variable = next((x for x in variableList if x.getName() == codeStringSplit[1]), None)
        if variable is None:
            raise ValueError("Nonexistent Variable")

        return cls(variable)


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

    @classmethod
    @abstractmethod
    def factoryMethod(cls, codeString, variableList):
        codeStringSplit = codeString.split()

        result = next((x for x in variableList if x.getName() == codeStringSplit[1]), None)
        if result is None:
            raise ValueError("Nonexistent Variable")

        if codeStringSplit[2].isnumeric():
            operand = Constant(int(codeStringSplit[2]))
        else:
            operand = next((x for x in variableList if x.getName() == codeStringSplit[2]), None)
            if operand is None:
                raise ValueError("Nonexistent Variable")

        return cls(result, operand)


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

    @classmethod
    def factoryMethod(cls, codeString, variableList):
        codeStringSplit = codeString.split()

        result = next((x for x in variableList if x.getName() == codeStringSplit[1]), None)
        if result is None:
            raise ValueError("Nonexistent Variable")

        if codeStringSplit[2].isnumeric():
            operand1 = Constant(int(codeStringSplit[2]))
        else:
            operand1 = next((x for x in variableList if x.getName() == codeStringSplit[2]), None)
            if operand1 is None:
                raise ValueError("Nonexistent Variable")

        if codeStringSplit[3].isnumeric():
            operand2 = Constant(int(codeStringSplit[3]))
        else:
            operand2 = next((x for x in variableList if x.getName() == codeStringSplit[3]), None)
            if operand2 is None:
                raise ValueError("Nonexistent Variable")

        return cls(result, operand1, operand2)


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
        if self.operand2.getValue() == 0:
            raise ValueError("Can't divide by zero")
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
        ModBlock.getBlockText(): ModBlock,
        PrintBlock.getBlockText(): PrintBlock
    }.get(text.split()[0], Block)
