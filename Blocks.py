from abc import abstractmethod

from Dialogs import *
from Variable import *


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

    def __init__(self, variable, printLog):
        self.variable = variable
        self.printLog = printLog

    def execute(self):
        self.printLog.append(str(self.variable.getValue()))

    @classmethod
    def getBlockText(cls):
        return "Print"

    @classmethod
    def clickAction(cls, qWidget, item):
        dialog = PrintInputDialog(qWidget, item)
        dialog.exec()

    @classmethod
    def factoryMethod(cls, codeString, variableList):
        codeStringSplit = codeString.split()

        if codeStringSplit[1].isnumeric():
            variable = Constant(int(codeStringSplit[1]))
        else:
            variable = next((x for x in variableList if x.getName() == codeStringSplit[1]), None)
            if variable is None:
                raise ValueError("Nonexistent Variable")

        printLog = next((x for x in variableList if x.getName() == "printLog"), None)
        if variable is None:
            raise ValueError("ERROR")

        return cls(variable, printLog)


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
        if self.operand2.getValue() == 0:
            raise ValueError("Can't mod by zero")
        self.result.setValue(self.operand1.getValue() % self.operand2.getValue())

    @classmethod
    def getBlockText(cls):
        return "Mod"


class IfBlock(Block):

    def __init__(self, value1, value2, comparisonOperator, instrIndex, endIndex):
        self.value1 = value1
        self.value2 = value2
        self.comparisonOperator = comparisonOperator
        self.instrIndex = instrIndex
        self.endIndex = endIndex

    def execute(self):
        if not evaluateBooleanExpression(self.value1.getValue(), self.value2.getValue(), self.comparisonOperator):
            self.instrIndex.setValue(self.endIndex.getValue())

    @classmethod
    def getBlockText(cls):
        return "If"

    @classmethod
    def clickAction(cls, qWidget, item):
        dialog = DecisionBlockDialog(qWidget, item, cls.getBlockText())
        dialog.exec()

    @classmethod
    def factoryMethod(cls, codeString, variableList):
        codeStringSplit = codeString.split()

        instrIndex = next((x for x in variableList if x.getName() == "instrIndex"), None)
        if instrIndex is None:
            raise ValueError("Nonexistent Variable")

        if codeStringSplit[1].isnumeric():
            operand1 = Constant(int(codeStringSplit[1]))
        else:
            operand1 = next((x for x in variableList if x.getName() == codeStringSplit[1]), None)
            if operand1 is None:
                raise ValueError("Nonexistent Variable")

        comparisonOperator = codeStringSplit[2]
        if comparisonOperator not in ["=", "!=", "<", ">", "<=", ">="]:
            raise ValueError("If Error")

        if codeStringSplit[3].isnumeric():
            operand2 = Constant(int(codeStringSplit[3]))
        else:
            operand2 = next((x for x in variableList if x.getName() == codeStringSplit[3]), None)
            if operand1 is None:
                raise ValueError("Nonexistent Variable")

        if codeStringSplit[4].isnumeric():
            endIndex = Constant(int(codeStringSplit[4]))
        else:
            raise ValueError("If Error")

        return cls(operand1, operand2, comparisonOperator, instrIndex, endIndex)


class EndIfBlock(Block):

    def __init__(self):
        pass

    def execute(self):
        pass

    @classmethod
    def getBlockText(cls):
        return "EndIf"

    @classmethod
    def clickAction(cls, qWidget, item):
        dialog = DeleteItemDialog(qWidget, item)
        dialog.exec()

    @classmethod
    def factoryMethod(cls, codeString, variableList):
        return cls()


class WhileBlock(Block):

    def __init__(self, value1, value2, comparisonOperator, instrIndex, endIndex):
        self.value1 = value1
        self.value2 = value2
        self.comparisonOperator = comparisonOperator
        self.instrIndex = instrIndex
        self.endIndex = endIndex

    def execute(self):
        if not evaluateBooleanExpression(self.value1.getValue(), self.value2.getValue(), self.comparisonOperator):
            self.instrIndex.setValue(self.endIndex.getValue())

    @classmethod
    def getBlockText(cls):
        return "While"

    @classmethod
    def clickAction(cls, qWidget, item):
        dialog = DecisionBlockDialog(qWidget, item, cls.getBlockText())
        dialog.exec()

    @classmethod
    def factoryMethod(cls, codeString, variableList):
        codeStringSplit = codeString.split()

        instrIndex = next((x for x in variableList if x.getName() == "instrIndex"), None)
        if instrIndex is None:
            raise ValueError("Nonexistent Variable")

        if codeStringSplit[1].isnumeric():
            operand1 = Constant(int(codeStringSplit[1]))
        else:
            operand1 = next((x for x in variableList if x.getName() == codeStringSplit[1]), None)
            if operand1 is None:
                raise ValueError("Nonexistent Variable")

        comparisonOperator = codeStringSplit[2]
        if comparisonOperator not in ["=", "!=", "<", ">", "<=", ">="]:
            raise ValueError("While Error")

        if codeStringSplit[3].isnumeric():
            operand2 = Constant(int(codeStringSplit[3]))
        else:
            operand2 = next((x for x in variableList if x.getName() == codeStringSplit[3]), None)
            if operand1 is None:
                raise ValueError("Nonexistent Variable")

        if codeStringSplit[4].isnumeric():
            endIndex = Constant(int(codeStringSplit[4]))
        else:
            raise ValueError("While Error")

        return cls(operand1, operand2, comparisonOperator, instrIndex, endIndex)


class EndWhileBlock(Block):

    def __init__(self, value1, value2, comparisonOperator, instrIndex, startIndex):
        self.value1 = value1
        self.value2 = value2
        self.comparisonOperator = comparisonOperator
        self.instrIndex = instrIndex
        self.startIndex = startIndex

    def execute(self):
        if evaluateBooleanExpression(self.value1.getValue(), self.value2.getValue(), self.comparisonOperator):
            self.instrIndex.setValue(self.startIndex.getValue())

    @classmethod
    def getBlockText(cls):
        return "EndWhile"

    @classmethod
    def clickAction(cls, qWidget, item):
        dialog = DeleteItemDialog(qWidget, item)
        dialog.exec()

    @classmethod
    def factoryMethod(cls, codeString, variableList):
        codeStringSplit = codeString.split()

        instrIndex = next((x for x in variableList if x.getName() == "instrIndex"), None)
        if instrIndex is None:
            raise ValueError("Nonexistent Variable")

        if codeStringSplit[2].isnumeric():
            operand1 = Constant(int(codeStringSplit[2]))
        else:
            operand1 = next((x for x in variableList if x.getName() == codeStringSplit[2]), None)
            if operand1 is None:
                raise ValueError("Nonexistent Variable")

        comparisonOperator = codeStringSplit[3]
        if comparisonOperator not in ["=", "!=", "<", ">", "<=", ">="]:
            raise ValueError("While Error")

        if codeStringSplit[4].isnumeric():
            operand2 = Constant(int(codeStringSplit[4]))
        else:
            operand2 = next((x for x in variableList if x.getName() == codeStringSplit[4]), None)
            if operand1 is None:
                raise ValueError("Nonexistent Variable")

        if codeStringSplit[5].isnumeric():
            startIndex = Constant(int(codeStringSplit[5]))
        else:
            raise ValueError("While Error")

        return cls(operand1, operand2, comparisonOperator, instrIndex, startIndex)


def getClassFromText(text):
    return {
        AssignmentBlock.getBlockText(): AssignmentBlock,
        AddBlock.getBlockText(): AddBlock,
        SubtractBlock.getBlockText(): SubtractBlock,
        MultiplyBlock.getBlockText(): MultiplyBlock,
        DivideBlock.getBlockText(): DivideBlock,
        ModBlock.getBlockText(): ModBlock,
        PrintBlock.getBlockText(): PrintBlock,
        IfBlock.getBlockText(): IfBlock,
        EndIfBlock.getBlockText(): EndIfBlock,
        WhileBlock.getBlockText(): WhileBlock,
        EndWhileBlock.getBlockText(): EndWhileBlock
    }.get(text.split()[0], Block)


def evaluateBooleanExpression(value1, value2, comparisonOperator):
    if comparisonOperator == "=":
        return value1 == value2

    if comparisonOperator == "!=":
        return value1 != value2

    if comparisonOperator == "<=":
        return value1 <= value2

    if comparisonOperator == ">=":
        return value1 >= value2

    if comparisonOperator == "<":
        return value1 < value2

    if comparisonOperator == ">":
        return value1 > value2
