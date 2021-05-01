import sys, os
from subprocess import Popen, PIPE

rootPath = os.getcwd()
customEnv = os.environ.copy()
customEnv["ANTLR_JAR"] = rootPath + "/antlr-4.8-complete.jar"

def main(argv):
    if len(argv) != 1:
        printUsage()
    elif argv[0] == 'gen':
        Popen(["python","run.py","gen"], env=customEnv).wait()
    elif argv[0] == 'clean':
        Popen(["python","run.py","clean"], env=customEnv).wait()
        Popen(["rm","-rf","./LexerSuite.log"])
        Popen(["rm","-rf","./ParserSuite.log"])
    elif argv[0] in ['lexer','onlylexer']:
        if argv[0] == 'lexer':
            Popen(["python","run.py","gen"], env=customEnv).wait()
        test("LexerSuite")
    elif argv[0] in ['parser','onlyparser']:
        if argv[0] == 'parser':
            Popen(["python","run.py","gen"], env=customEnv).wait()
        test("ParserSuite")
    else:
        printUsage()

class unittest:
    class TestCase:
        def assertTrue(self, check):
            if check != "":
                print(check)

class TestLexer:
    @classmethod
    def checkLexeme(cls, inputStr, expectStr, testcase):
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

class TestParser:
    @classmethod
    def checkParser(cls, inputStr, expectStr, testcase):
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

def test(testName):
    # generate solution
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
    # print test debug
    print("FAILED TESTCASE LIST")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    testSuiteClass = "class " + testName + ": pass"
    with open(rootPath + "/test/" + testName + ".py") as f:
        s = f.read()
        beginClass = s.find("class " + testName)
        testSuiteClass = s[beginClass:]
    exec(testSuiteClass)
    testSuite = eval(testName+"()")
    testList = [method for method in dir(eval(testName)) if method.startswith("test") is True]
    for test in testList:
        funcTest = getattr(testSuite, test)()
    # print runtime
    runtime = logStr[-5:-1]
    for line in runtime:
        print(line)

def printUsage():
    print("python debug.py gen")
    print("python debug.py lexer")
    print("python debug.py onlylexer")
    print("python debug.py parser")
    print("python debug.py onlyparser")
    print("python debug.py clean")

if __name__ == "__main__":
   main(sys.argv[1:])
