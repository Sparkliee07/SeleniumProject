import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from ATLAS.framework.api.TestSiteLib.TestStatus import TestStatus
from ATLAS.framework.api.TestSiteLib.AbortException import AbortException
from ATLAS.framework.api.TestSiteLib.ParallelValue import ParallelValue
from ATLAS.framework.api.TestSiteLib.CompareOptions import CompareOptions

class BaseTest:
    TEST_PARAMS_COMMON_FILENAME = "TestParamsCommon.xml"
    TEST_PARAMS_FILENAME = "TestParams.xml"
    CONSOLE_WIDTH = 120
    CONSOLE_HEIGHT = 60
    CONSOLE_BUFFER_LENGTH = 32000

    def __init__(self):
        self.TestsToRun = "*"
        self.SuiteLoopCount = 1
        self.Verbose = False
        self.FailToDo = False
        self.AllowSkipAllTests = False
        self.TsarFilePathWindows = "..\\..\\..\\..\\..\\..\\TestSiteRunner\\bin\\Debug\\net6.0\\TestSiteRunner.exe"
        self.TsarFilePathLinux = "..\\..\\..\\..\\..\\..\\TestSiteRunner\\bin\\Release\\net6.0\\publish\\linux-x64\\TestSiteRunner"

        self._testStatus = ParallelValue(False, TestStatus.Pass)
        self._suiteStatus = TestStatus.Pass
        self._tests = []
        self._testMethods = []
        self.SltPlatform = "All"
        self.SubSltPlatform = "None"
        self._results = {}
        self._times = {}
        self._suiteStart = datetime.min
        self._timerStart = ParallelValue(False, datetime.min)
        self._customOptions = CompareOptions.None_

        try:
            self.Init()
            self.Start()
            self.LoopSuite()
        except AbortException:
            self.LogResult(TestStatus.FAIL, "Test aborted.")
        except Exception as ex:
            self.LogResult(TestStatus.FAIL, "Exception", "Type:", type(ex).__name__, "Message:", str(ex))
        finally:
            self.Finish()

    def Init(self):
        pass

    @property
    def Status(self):
        return int(self._suiteStatus)

    @property
    def TestName(self):
        return os.path.basename(__file__)

    @property
    def IterationList(self):
        return None

    @property
    def IterationName(self):
        return "index"

    @property
    def IterationNamePlural(self):
        return "indices"

    @property
    def SetUpIterationName(self):
        return "SetUpIteration"

    @property
    def TearDownIterationName(self):
        return "TearDownIteration"

    @property
    def Iteration(self):
        return self._iteration

    @Iteration.setter
    def Iteration(self, value):
        self._iteration.value = value

    @property
    def IsParallel(self):
        return False

    def Start(self):
        if os.getenv('DEBUG'):
            pass  # Console settings can be applied here if needed

        self.InitLog()
        self.Subsection("Initialize")

        # Directory creation and parameter reading can be added here if needed

        # Run update procedure after reading Params
        self.Update()

    def Update(self):
        pass

    def GetTestParamsFile(self):
        executable_name = os.path.splitext(os.path.basename(__file__))[0]
        xml_file_name = f"{executable_name}.xml"

        if os.path.exists(xml_file_name):
            return xml_file_name

        if os.path.exists(self.TEST_PARAMS_FILENAME):
            return self.TEST_PARAMS_FILENAME

        return None

    def ReadParams(self):
        self.Subsection("Test parameters")

        # Log suite details here

        props = [attr for attr in dir(self) if isinstance(getattr(type(self), attr, None), property)]

        test_params_file = self.GetTestParamsFile()

        common_path = None
        for dirpath, _, _ in os.walk(os.getcwd()):
            path = os.path.join(dirpath, self.TEST_PARAMS_COMMON_FILENAME)
            if os.path.exists(path):
                common_path = path
                break

        if not test_params_file:
            self.LogResult(TestStatus.FAIL, f"{self.TEST_PARAMS_FILENAME} not found.")

        if not common_path:
            self.LogResult(TestStatus.FAIL, f"{self.TEST_PARAMS_COMMON_FILENAME} not found.")

        xml_common_tree = ET.parse(common_path) if common_path else None

        status = TestStatus.Pass

        for prop in props:
            name = prop
            value = None

            # Command line argument parsing can be added here

            element_common = xml_common_tree.find(name) if xml_common_tree else None

            if element_common is None:
                status = self.LogResult(TestStatus.FAIL, name, "Error:", "Parameter missing")
                continue

            attribute_common_value = element_common.get("value") if element_common is not None else None

            if attribute_common_value is None:
                status = self.LogResult(TestStatus.FAIL, name, "Error:", "Value missing")
                continue

            value = attribute_common_value

            try:
                obj_value = value  # Parsing logic can be added here based on property type

                setattr(self, prop, obj_value)

                # Logging logic can be added here

            except Exception as ex:
                status = self.LogResult(TestStatus.FAIL, name, "Error:", str(ex))

        if status == TestStatus.FAIL:
            self.Abort()

    def ParseXml(self, path):
        try:
            if path is None:
                return None

            tree = ET.parse(path)
            return tree.getroot()

        except Exception as ex:
            self.LogResult(TestStatus.FAIL, "XML error", "Error:", str(ex))
            self.Abort()

    def SetUp(self):
        pass

    def SetUpIteration(self):
        pass

    def TearDownIteration(self):
        pass

    def TearDown(self):
        pass

    def PreTestStep(self):
        pass

    def PostTestStep(self):
        pass

    def PreSuiteStep(self):
        pass

    def PostSuiteStep(self):
        pass

    def Finish(self):
        if os.getenv('DEBUG'):
            print("\nPress any key.")

    def Do(self, message, action, suppressPass=False):
        try:
            action()
            if not suppressPass:
                self.LogResult(TestStatus.Pass, message)
        except Exception as ex:
            self.LogResult(TestStatus.FAIL, message, "Error:", str(ex))
            raise ex

    def LogResult(self, status, *args):
        # Placeholder for logging method
        print(f"Status: {status}, Details: {args}")


