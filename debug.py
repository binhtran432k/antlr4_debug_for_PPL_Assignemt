import sys, os
from subprocess import Popen, PIPE
import traceback
import importlib.util

rootPath = os.getcwd()
customEnv = os.environ.copy()
customEnv["ANTLR_JAR"] = rootPath + "/antlr-4.8-complete.jar"

locpath = ['./main/csel/parser/','./main/csel/astgen/','./main/csel/utils/','./test/','../target/main/csel/parser']
for p in locpath:
    if not p in sys.path:
        sys.path.append(p)
# import AST if exists
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
        test("ASTGenSuite",notUseRun=False)
    else:
        printUsage()

class unittest:
    class TestCase:
        def assertTrue(self, check):
            if check != "":
                print(check)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def checkCommon(inputStr, expectStr, testcase, outputStr=None):
    if outputStr == None:
        outputStr = ""
        with open(rootPath + "/test/solutions/" + str(testcase) + ".txt") as f:
            outputStr = f.read()
    if outputStr == expectStr:
        return ""
    else:
        output = "-----------------Testcase " + str(testcase) + "------------------\n"
        output += bcolors.HEADER + "Input:\n" + bcolors.ENDC
        output += inputStr + "\n"
        output += bcolors.HEADER + "Output:\n" + bcolors.ENDC
        output += bcolors.FAIL + outputStr + "\n" + bcolors.ENDC
        output += bcolors.HEADER + "Expect:\n" + bcolors.ENDC
        output += bcolors.WARNING + expectStr + "\n" + bcolors.ENDC
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
        from TestUtils import TestAST as realTestAST
        try:
            realTestAST.checkASTGen(inputStr, expectStr, testcase)
        except Exception as e:
            track = traceback.format_exc()
            return checkCommon(inputStr, str(expectStr), testcase, outputStr=track)
        return checkCommon(inputStr, str(expectStr), testcase)

def test(testName, useAsRun=False, notUseRun=True):
    if notUseRun:
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
    else:
        logStr = [""]
    testSuiteClass = "class " + testName + ": pass"
    with open(rootPath + "/test/" + testName + ".py") as f:
        s = f.read()
        beginClass = s.find("class " + testName)
        testSuiteClass = s[beginClass:]
    exec(testSuiteClass)
    testSuite = eval(testName+"()")
    testList = [method for method in dir(eval(testName)) if method.startswith("test") is True]
    # print test debug
    runtime = logStr[-4:-1]
    success = False
    for line in runtime:
        if line.find("OK") != -1:
            success = True
            break
    if not success:
        print(bcolors.FAIL+"FAILED TESTCASE LIST")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"+bcolors.ENDC)
    for test in testList:
        getattr(testSuite, test)()
    # print runtime
    if success:
        print(bcolors.OKGREEN, end='')
    else:
        print(bcolors.FAIL, end='')
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    for line in runtime:
        print(line)
    print(bcolors.ENDC, end='')

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
