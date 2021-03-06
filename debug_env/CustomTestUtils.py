from .bcolors import bcolors
import traceback

from os import getcwd
workPath = getcwd()

# import TestUtils if exists
try:
    import TestUtils
    RealTest = TestUtils
except:
    print(bcolors.WARNING+"Warning: TestUtils is broken. Cannot get RealTest!"+bcolors.ENDC)
    class RealTest: pass
    pass

def checkCommon(inputStr, expectStr, testcase, outputStr=None):
    if outputStr == None:
        outputStr = ""
        with open(workPath+"/test/solutions/" + str(testcase) + ".txt") as f:
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

class CustomTestUtils:
    class TestLexer:
        @staticmethod
        def checkLexeme(inputStr, expectStr, testcase):
            try:
                RealTest.TestLexer.checkLexeme(inputStr, expectStr, testcase)
            except:
                track = traceback.format_exc()
                print(checkCommon(inputStr, str(expectStr), testcase, track))
                raise
            return checkCommon(inputStr, expectStr, testcase)
    class TestParser:
        @staticmethod
        def checkParser(inputStr, expectStr, testcase):
            try:
                RealTest.TestParser.checkParser(inputStr, expectStr, testcase)
            except:
                track = traceback.format_exc()
                print(checkCommon(inputStr, str(expectStr), testcase, track))
                raise
            return checkCommon(inputStr, expectStr, testcase)
    class TestAST:
        @staticmethod
        def checkASTGen(inputStr, expectStr, testcase):
            try:
                RealTest.TestAST.checkASTGen(inputStr, expectStr, testcase)
            except:
                track = traceback.format_exc()
                print(checkCommon(inputStr, str(expectStr), testcase, track))
                raise
            return checkCommon(inputStr, str(expectStr), testcase)
    class TestChecker:
        @staticmethod
        def test(input,expect,num):
            return CustomTestUtils.TestChecker.checkStatic(input,expect,num)
        @staticmethod
        def checkStatic(input, expectStr, testcase):
            if type(input) is str:
                inputStr = input
            else:
                inputStr = str(input)
            try:
                RealTest.TestChecker.test(input, expectStr, testcase)
            except:
                track = traceback.format_exc()
                print(checkCommon(inputStr, str(expectStr), testcase, track))
                raise
            return checkCommon(inputStr, str(expectStr), testcase)