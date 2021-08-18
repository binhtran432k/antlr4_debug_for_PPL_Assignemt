import json, os
from os.path import normpath
def getOption(testName, command, isOnly):
    if isOnly:
        testName = "Only "+testName
        command = "only"+command
    return {
        "name": f"Python: Debug {testName}",
        "type": "python",
        "request": "launch",
        "program": "${workspaceFolder}"+os.path.normpath("/debug.py"),
        "console": "integratedTerminal",
        "args": [f"{command}"]
    }
def generateDebug():
    from .settings import languageName, locpath
    extraPaths = ["${workspaceFolder}" + os.path.normpath("/src/" + x) for x in locpath]
    extraPaths.append("${workspaceFolder}"+os.path.normpath("/debug_env/"))
    settings = {
        "python.autoComplete.extraPaths": extraPaths,
        "python.analysis.extraPaths": extraPaths,
        "debug.terminal.clearBeforeReusing": True
    }
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Antlr4: Debug ANTLR4 grammar",
                "type": "antlr-debug",
                "request": "launch",
                "input": "${workspaceFolder}"+os.path.normpath("/input.txt"),
                "grammar": "${workspaceFolder}"+os.path.normpath(f"/src/main/{languageName}/parser/{languageName.upper()}.g4"),
                "startRule": "program",
                "printParseTree": True,
                "visualParseTree": True
            }
        ]
    }

    testNameList = ["LexerSuiet","ParserSuite","ASTGenSuite","CheckSuite"]
    commandList = ["lexer","parser","ast","check"]
    testList = list(map(lambda x, y: (x, y), testNameList, commandList))
    typList = [False,True]
    for typ in typList:
        for test in testList:
            launch["configurations"].append(getOption(test[0], test[1], typ))

    if not os.path.exists('../.vscode'):
        os.makedirs('../.vscode')
    with open('../.vscode/settings.json','w') as f:
        f.write(json.dumps(settings, indent=4))
    with open('../.vscode/launch.json','w') as f:
        f.write(json.dumps(launch, indent=4))