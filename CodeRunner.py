from Blocks import getClassFromText
from Variable import Variable


def runCode(codeStringList, variables):
    code = []

    instrIndex = Variable(0, "instrIndex")
    variables.append(instrIndex)

    if any(map(lambda x: x.__contains__("..."), codeStringList)):
        raise ValueError("Incomplete specification")

    for codeString in codeStringList:
        code.append(getClassFromText(codeString).factoryMethod(codeString, variables))

    for instruction in code:
        instruction.execute()
