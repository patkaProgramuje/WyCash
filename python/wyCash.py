class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self, result):
        result.testStarted()
        self.setUp()
        try:
            method = getattr(self, self.name)
            method()
        except:
            result.testFailed()
        self.tearDown()

    def setUp(self):
        pass

    def tearDown(self):
        pass


class WasRun(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def setUp(self):
        self.log = "setUp "

    def testMethod(self):
        self.log = self.log + "testMethod "

    def tearDown(self):
        self.log = self.log + "tearDown "

    def testBrokenMethod(self):
        raise Exception


class TestCaseTest(TestCase):
    def setUp(self):
        self.test = TestResult()

    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run(result)
        assert ("setUp testMethod tearDown " == test.log)

    def testResult(self):
        test = WasRun("testMethod")
        test.run(result)
        assert ("1 run, 0 failed" == result.summary())

    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        test.run(result)
        assert "1 run, 1 failed", result.summary()

    def testFailedResultFormatting(self):
        result.testStarted()
        result.testFailed()
        assert "1 run, 1 failed" == result.summary()

    def testSuite(self):
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.run(result)
        assert "2 run, 1 failed" == result.summary()


class TestSuite:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class TestResult:
    def __init__(self):
        self.runCount = 0
        self.errorCount = 0

    def testFailed(self):
        self.errorCount = self.errorCount + 1

    def testStarted(self):
        self.runCount = self.runCount + 1

    def summary(self):
        return "%d run, %d failed" % (self.runCount, self.errorCount)


suite = TestSuite()
print(TestCaseTest("testTemplateMethod"))
print(TestCaseTest("testResult"))
print(TestCaseTest("testFailedResultFormatting"))
print(TestCaseTest("testFailedResult"))
print(TestCaseTest("testSuite"))
result = TestResult()
suite.run(result)
print(result.summary())
