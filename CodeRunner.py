from Blocks import getClassFromText


def runCode(codeStringList, variables):
    code = []

    if any(map(lambda x: x.__contains__("..."), codeStringList)):
        raise ValueError("Incomplete specification")

    for codeString in codeStringList:
        code.append(getClassFromText(codeString).factoryMethod(codeString, variables))

    for instruction in code:
        instruction.execute()
