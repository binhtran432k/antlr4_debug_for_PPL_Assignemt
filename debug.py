import sys, os
from subprocess import run as subRun

rootPath = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(rootPath+'/debug_env')

import antlr4
sys.modules["antlr4"] = antlr4
os.environ["ANTLR_JAR"] = rootPath + "/debug_env/antlr-4.8-complete.jar"
workPath = rootPath+"/src/"
os.chdir(workPath)

from debug_env.settings import locpath
for p in locpath:
    p = workPath+p
    if not p in sys.path:
        sys.path.append(p)

from debug_env.CustomUnittest import CustomUnittest
from debug_env.CustomTestUtils import CustomTestUtils

def main(argv):
    if (len(argv) == 1 and argv[0] in ["gen","clean"]) or (len(argv) == 2 and argv[0] == "test"
    and (argv[1] in ["LexerSuite","ParserSuite","ASTGenSuite","CheckSuite"])):
        from src.run import main as run
        run(argv)
        if (argv[0] == "clean"):
            subRun(["rm","-rf","../.vscode"])
    else:
        sys.modules["unittest"] = CustomUnittest
        sys.modules["TestUtils"] = CustomTestUtils
        from src.run import main as run
        if len(argv) != 1:
            printUsage()
        elif argv[0] in ['lexer','onlylexer']:
            if argv[0] == 'lexer':
                run(['gen'])
                subRun(["python","../debug.py","onlylexer"])
            else:
                run(['test','LexerSuite'])
        elif argv[0] in ['parser','onlyparser']:
            if argv[0] == 'parser':
                run(['gen'])
                subRun(["python","../debug.py","onlyparser"])
            else:
                run(['test','ParserSuite'])
        elif argv[0] in ['ast','onlyast']:
            if argv[0] == 'ast':
                run(['gen'])
                subRun(["python","../debug.py","onlyast"])
            else:
                run(['test','ASTGenSuite'])
        elif argv[0] in ['check','onlycheck']:
            if argv[0] == 'check':
                run(['gen'])
                subRun(["python","../debug.py","onlycheck"])
            else:
                run(['test','CheckSuite'])
        elif argv[0] == 'vscode':
            from debug_env.vscode import generateDebug
            generateDebug()
        else:
            printUsage()

def printUsage():
    print("-------Original-------")
    print("python debug.py gen")
    print("python debug.py clean")
    print("python debug.py test LexerSuite")
    print("python debug.py test ParserSuite")
    print("python debug.py test ASTGenSuite")
    print("python debug.py test CheckSuite")
    print("-------Customize-------")
    print("python debug.py lexer")
    print("python debug.py parser")
    print("python debug.py ast")
    print("python debug.py check")
    print("python debug.py onlylexer")
    print("python debug.py onlyparser")
    print("python debug.py onlyast")
    print("python debug.py onlycheck")
    print("-------Vscode Debug and Hint-------")
    print("python debug.py vscode")

if __name__ == "__main__":
    main(sys.argv[1:])
