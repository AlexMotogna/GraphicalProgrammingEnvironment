from abc import abstractmethod


class Block:

    @abstractmethod
    def execute(self):
        pass


class AssignmentBlock(Block):

    def __init__(self, result, operand):
        self.result = result
        self.operand = operand

    def execute(self):
        self.result.setValue(self.operand.getValue())


class TwoOperandBlock(Block):

    def __init__(self, result, operand1, operand2):
        self.result = result
        self.operand1 = operand1
        self.operand2 = operand2

    @abstractmethod
    def execute(self):
        pass


class AddBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() + self.operand2.getValue())


class SubtractBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() - self.operand2.getValue())


class MultiplyBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() * self.operand2.getValue())


class DivideBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() / self.operand2.getValue())


class ModBlock(TwoOperandBlock):

    def __init__(self, result, operand1, operand2):
        super().__init__(result, operand1, operand2)

    def execute(self):
        self.result.setValue(self.operand1.getValue() % self.operand2.getValue())
