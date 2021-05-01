import sys, os
from subprocess import Popen, PIPE

rootPath = os.getcwd()
customEnv = os.environ.copy()
customEnv["ANTLR_JAR"] = rootPath + "/antlr-4.8-complete.jar"

locpath = ['./main/csel/parser/','./main/csel/astgen/','./main/csel/utils/']
for p in locpath:
    if not p in sys.path:
        sys.path.append(p)
# import AST if exists
import importlib.util
if importlib.util.find_spec('AST') is not None:
    from AST import *

def main(argv):
    if len(argv) != 1:
        if argv[0] == 'test':
            if len(argv) < 2:
                printUsage()
            elif argv[1] == 'LexerSuite':
                test("LexerSuite",True)
            elif argv[1] == 'ParserSuite':
                test("ParserSuite",True)
            elif argv[1] == 'ASTGenSuite':
                test("ASTGenSuite",True)
            else:
                printUsage()
        else:
            printUsage()
    elif argv[0] == 'gen':
        Popen(["python","run.py","gen"], env=customEnv).wait()
    elif argv[0] == 'clean':
        Popen(["python","run.py","clean"], env=customEnv).wait()
        Popen(["rm","-rf","./LexerSuite.log"])
        Popen(["rm","-rf","./ParserSuite.log"])
        Popen(["rm","-rf","./ASTGenSuite.log"])
    elif argv[0] in ['lexer','onlylexer']:
        if argv[0] == 'lexer':
            Popen(["python","run.py","gen"], env=customEnv).wait()
        test("LexerSuite")
    elif argv[0] in ['parser','onlyparser']:
        if argv[0] == 'parser':
            Popen(["python","run.py","gen"], env=customEnv).wait()
        test("ParserSuite")
    elif argv[0] in ['ast','onlyast']:
        if argv[0] == 'ast':
            Popen(["python","run.py","gen"], env=customEnv).wait()
        test("ASTGenSuite")
    else:
        printUsage()

class unittest:
    class TestCase:
        def assertTrue(self, check):
            if check != "":
                print(check)

def checkCommon(inputStr, expectStr, testcase):
    outputStr = ""
    with open(rootPath + "/test/solutions/" + str(testcase) + ".txt") as f:
        outputStr = f.read()
    if outputStr == expectStr:
        return ""
    else:
        output = "-----------------Testcase " + str(testcase) + "------------------\n"
        output += "Input:\n"
        output += inputStr + "\n"
        output += "Output:\n"
        output += outputStr + "\n"
        output += "Expect:\n"
        output += expectStr + "\n"
        output += "=================================================\n"
        return output

class TestLexer:
    @staticmethod
    def checkLexeme(inputStr, expectStr, testcase):
        return checkCommon(inputStr, expectStr, testcase)

class TestParser:
    @staticmethod
    def checkParser(inputStr, expectStr, testcase):
        return checkCommon(inputStr, expectStr, testcase)

class TestAST:
    @staticmethod
    def checkASTGen(inputStr, expectStr, testcase):
        return checkCommon(inputStr, str(expectStr), testcase)

def test(testName, useAsRun=False):
    # generate solution
    if useAsRun:
        Popen(["python","run.py","test",testName], env=customEnv).wait()
        return
    testLog = Popen(["python","run.py","test",testName], env=customEnv, stdout=PIPE, stderr=PIPE)
    out, err = testLog.communicate()
    testLog.wait()
    if err:
        print(err.decode('utf-8'))
        return
    # write log
    with open(rootPath + "/" + testName + ".log", "wb") as f:
        f.write(out)
    # store log
    logStr = out.decode('utf-8').splitlines()
    testSuiteClass = "class " + testName + ": pass"
    with open(rootPath + "/test/" + testName + ".py") as f:
        s = f.read()
        beginClass = s.find("class " + testName)
        testSuiteClass = s[beginClass:]
    exec(testSuiteClass)
    testSuite = eval(testName+"()")
    testList = [method for method in dir(eval(testName)) if method.startswith("test") is True]
    # print test debug
    runtime = logStr[-5:-1]
    success = False
    for line in runtime:
        if line.find("OK") != -1:
            success = True
            break
    if success:
        print("FAILED TESTCASE LIST")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    for test in testList:
        funcTest = getattr(testSuite, test)()
    # print runtime
    for line in runtime:
        print(line)

def printUsage():
    print("python debug.py gen")
    print("python debug.py lexer")
    print("python debug.py onlylexer")
    print("python debug.py parser")
    print("python debug.py onlyparser")
    print("python debug.py ast")
    print("python debug.py onlyast")
    print("python debug.py clean")
    print("python debug.py test LexerSuite")
    print("python debug.py test ParserSuite")
    print("python debug.py test ASTGenSuite")

if __name__ == "__main__":
   main(sys.argv[1:])
