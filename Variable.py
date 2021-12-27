class Constant:

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value


class Variable(Constant):

    def __init__(self, value, name):
        super().__init__(value)
        self.name = name

    def getName(self):
        return self.name

    def setValue(self, newValue):
        self.value = newValue


class PrintLog(Variable):

    def __init__(self, name):
        super().__init__("", name)

    def append(self, string):
        self.value += string
        self.value += "\n"
