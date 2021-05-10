import json, os
def getOption(testName, command, isOnly):
    if isOnly:
        testName = "Only "+testName
        command = "only"+command
    return {
        "name": f"Python: Debug {testName}",
        "type": "python",
        "request": "launch",
        "program": "${workspaceFolder}/debug.py",
        "console": "integratedTerminal",
        "args": [f"{command}"]
    }
def generateDebug():
    from .settings import languageName
    extraPaths = [
        f"${{workspaceFolder}}/src/main/{languageName}/astgen",
        f"${{workspaceFolder}}/src/main/{languageName}/checker",
        f"${{workspaceFolder}}/src/main/{languageName}/parser",
        f"${{workspaceFolder}}/src/main/{languageName}/utils",
        f"${{workspaceFolder}}/src/test",
        f"${{workspaceFolder}}/debug_env",
        f"${{workspaceFolder}}/target/main/{languageName}/parser"
    ]
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
                "input": "${workspaceFolder}/input.txt",
                "grammar": f"${{workspaceFolder}}/src/main/{languageName}/parser/{languageName.upper()}.g4",
                "startRule": "program",
                "printParseTree": True,
                "visualParseTree": True
            }
        ]
    }

    testNameList = ["LexerSuiet","ParserSuite","ASTGenSuite"]
    commandList = ["lexer","parser","ast"]
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