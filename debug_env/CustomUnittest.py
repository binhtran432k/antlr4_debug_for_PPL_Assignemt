from io import StringIO
from .bcolors import bcolors
import time

class CustomUnittest:
    stream: StringIO
    class TestCase:
        def __init__(self):
            self.testsRun = 0
            self.errors = 0
            self.failures = None
        def assertTrue(self, check):
            self.testsRun += 1
            if check != None:
                self.errors += 1
                CustomUnittest.stream.write(check)
    class TextTestRunner:
        def __init__(self, stream):
            CustomUnittest.stream = stream
        def run(self, suite):
            start = time.time()
            testList = [method for method in dir(suite) if method.startswith("test") is True]
            for test in testList:
                testObj = getattr(suite, test)
                if callable(testObj):
                    testObj()
            end = time.time()
            postStr = ''
            if suite.errors == 0:
                postStr += bcolors.OKGREEN
            else:
                postStr += bcolors.FAIL
            postStr += '------------------------------------------------------------------\n'
            postStr += "Ran "+str(suite.testsRun)+" test in "+"{0:.3f}s\n\n".format(end-start)
            if suite.errors == 0:
                postStr += "OK"
            else:
                postStr += "FAILED (errors="+str(suite.errors)+")"
            postStr += bcolors.ENDC
            CustomUnittest.stream.write(postStr)
            return suite
    @staticmethod
    def makeSuite(test):
        return test()