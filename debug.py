import sys, os, traceback, time, re
from subprocess import Popen

rootPath = os.getcwd()
customEnv = os.environ.copy()
customEnv["ANTLR_JAR"] = rootPath + "/antlr-4.8-complete.jar"

locpath = ['./main/csel/parser/','./main/csel/astgen/','./main/csel/utils/','./test/','../target/main/csel/parser']
for p in locpath:
    if not p in sys.path:
        sys.path.append(p)
# import AST if exists
warning = ""
try:
    from AST import *
except:
    warning += "Warning: AST not found. Cannot test AST!\n"
    pass
# import TestUtils if exists
try:
    import TestUtils as RealTest
except:
    warning += "Warning: TestUtils is broken. Cannot get RealTest!\n"
    pass

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
        testName = "LexerSuite"
        if argv[0] == 'lexer':
            Popen(["python","run.py","gen"], env=customEnv).wait()
            Popen(["python","debug.py","onlylexer"]).wait()
        else:
            test(testName)
    elif argv[0] in ['parser','onlyparser']:
        testName = "ParserSuite"
        if argv[0] == 'parser':
            Popen(["python","run.py","gen"], env=customEnv).wait()
            Popen(["python","debug.py","onlyparser"]).wait()
        else:
            test(testName)
    elif argv[0] in ['ast','onlyast']:
        testName = "ASTGenSuite"
        if argv[0] == 'ast':
            Popen(["python","run.py","gen"], env=customEnv).wait()
            Popen(["python","debug.py","onlyast"]).wait()
        else:
            test(testName)
    else:
        printUsage()

class unittest:
    class TestCase:
        unitCount = 0
        successCount = 0
        def assertTrue(self, check):
            unittest.TestCase.unitCount += 1
            if check != None:
                print(check)
            else:
                unittest.TestCase.successCount += 1

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
        return None
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

class TestUtils:
    class TestLexer:
        @staticmethod
        def checkLexeme(inputStr, expectStr, testcase):
            try:
                RealTest.TestLexer.checkLexeme(inputStr, expectStr, testcase)
            except:
                track = traceback.format_exc()
                return checkCommon(inputStr, str(expectStr), testcase, outputStr=track)
            return checkCommon(inputStr, expectStr, testcase)

    class TestParser:
        @staticmethod
        def checkParser(inputStr, expectStr, testcase):
            try:
                RealTest.TestParser.checkParser(inputStr, expectStr, testcase)
            except:
                track = traceback.format_exc()
                return checkCommon(inputStr, str(expectStr), testcase, outputStr=track)
            return checkCommon(inputStr, expectStr, testcase)

    class TestAST:
        @staticmethod
        def checkASTGen(inputStr, expectStr, testcase):
            try:
                RealTest.TestAST.checkASTGen(inputStr, expectStr, testcase)
            except:
                track = traceback.format_exc()
                return checkCommon(inputStr, str(expectStr), testcase, outputStr=track)
            return checkCommon(inputStr, str(expectStr), testcase)

def test(testName, useAsRun=False):
    oldStdout = sys.stdout
    log = open(testName+".log","w+")
    sys.stdout = log
    try:
        print(bcolors.WARNING+warning+bcolors.ENDC)
        if useAsRun:
            Popen(["python","run.py","test",testName], stderr=log, env=customEnv).wait()
        else:
            start = time.time()
            unittest.TestCase.unitCount = 0
            unittest.TestCase.successCount = 0
            #testSuiteClass = "class " + testName + ": pass"
            #with open(rootPath + "/test/" + testName + ".py") as f:
            #    s = f.read()
            #    beginClass = s.find("class " + testName)
            #    testSuiteClass = s[beginClass:]
            #exec(testSuiteClass)
            sys.modules["unittest"] = unittest
            sys.modules["TestUtils"] = TestUtils
            exec("from "+testName+" import "+testName)
            testSuite = eval(testName+"()")
            testList = [method for method in dir(eval(testName)) if method.startswith("test") is True]
            # print test debug
            for test in testList:
                getattr(testSuite, test)()
            end = time.time()
            # print runtime
            errorCount = unittest.TestCase.unitCount - unittest.TestCase.successCount
            if errorCount == 0:
                print(bcolors.OKGREEN, end='')
            else:
                print(bcolors.FAIL, end='')
                print("------------------------------------------------------------------")
            print("Ran "+str(unittest.TestCase.unitCount)+" test in "+"{0:.3f}s".format(end-start))
            print()
            if errorCount == 0:
                print("OK")
            else:
                print("FAILED (errors="+str(errorCount)+")")
            print(bcolors.ENDC, end='')
    except:
        track = traceback.format_exc()
        print(track)
    finally:
        sys.stdout = oldStdout
        log.seek(0)
        logPrint = log.read()
        print(logPrint, end="")
        log.close()
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        result = ansi_escape.sub('', logPrint)
        log = open(testName+".log","w")
        log.write(result)
        log.close()


def printUsage():
    print("python debug.py gen")
    print("python debug.py lexer")
    print("python debug.py parser")
    print("python debug.py ast")
    print("python debug.py onlylexer")
    print("python debug.py onlyparser")
    print("python debug.py onlyast")
    print("python debug.py clean")
    print("python debug.py test LexerSuite")
    print("python debug.py test ParserSuite")
    print("python debug.py test ASTGenSuite")

if __name__ == "__main__":
    main(sys.argv[1:])
