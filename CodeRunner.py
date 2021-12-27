from Blocks import *
from Variable import Variable


def runCode(codeStringList, variables):
    code = []

    instrIndex = Variable(0, "instrIndex")
    variables.append(instrIndex)

    printLog = PrintLog("printLog")
    variables.append(printLog)

    if any(map(lambda x: x.__contains__("..."), codeStringList)):
        raise ValueError("Incomplete specification")

    for i, codeString in enumerate(codeStringList):
        if getClassFromText(codeString) == IfBlock:
            stack = ["if"]
            j, lastElem = checkIfWhile(i, stack, codeStringList)

            if lastElem == "if":
                codeString += (" " + str(j - 1))
                codeStringList[j - 1] += " /"
            else:
                raise ValueError("Incorrect EndWhile placement")

        if getClassFromText(codeString) == EndIfBlock:
            if not codeString.__contains__("/"):
                raise ValueError("Too many EndIf Blocks")

        if getClassFromText(codeString) == WhileBlock:
            stack = ["while"]
            j, lastElem = checkIfWhile(i, stack, codeStringList)

            if lastElem == "while":
                codeStringList[j - 1] += (" " + codeString + " " + str(i) + " /")
                codeString += (" " + str(j - 1))
            else:
                raise ValueError("Incorrect EndIf placement")

        if getClassFromText(codeString) == EndWhileBlock:
            if not codeString.__contains__("/"):
                raise ValueError("Too many EndWhile Blocks")

        code.append(getClassFromText(codeString).factoryMethod(codeString, variables))

    while len(code) > instrIndex.getValue():
        code[instrIndex.getValue()].execute()
        instrIndex.setValue(instrIndex.getValue() + 1)

    alert = QMessageBox()
    alert.setWindowTitle("Print Log")
    alert.setText(printLog.getValue() + "Execution ended")
    alert.exec()


def checkIfWhile(i, stack, codeStringList):
    j = i + 1
    lastElem = None

    while len(stack) != 0:
        if j >= len(codeStringList):
            raise ValueError("Incorrect EndWhile placement")
        if getClassFromText(codeStringList[j]) == WhileBlock:
            stack.append("while")
        if getClassFromText(codeStringList[j]) == IfBlock:
            stack.append("if")
        if getClassFromText(codeStringList[j]) == EndIfBlock:
            if stack[-1] == "if":
                lastElem = stack.pop()
            else:
                raise ValueError("Incorrect EndIf placement")
        if getClassFromText(codeStringList[j]) == EndWhileBlock:
            if stack[-1] == "while":
                lastElem = stack.pop()
            else:
                raise ValueError("Incorrect EndWhile placement")
        j += 1

    return j, lastElem
