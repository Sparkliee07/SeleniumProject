import datetime
import time
import threading
from enum import Enum
import inspect
from ATLAS.framework.api.TestSiteLib.TestStatus import TestStatus
from ATLAS.framework.api.TestSiteLib.CompareOptions import CompareOptions



class BaseTest:
    def __init__(self):
        self.Verbose = True
        self.BeforeLoggingFailure = None

    def LogBusy(self, busy, message):
        print(f"{'Busy' if busy else 'Not busy'}: {message}")

    def LogResult(self, status, message, label, value):
        print(f"{status.name}: {message}, {label} {value}")

    def LogProgress(self, message, label, value):
        print(f"Progress - {message}: {label} {value}")

    def LogComplete(self, message, label, value):
        print(f"Complete - {message}: {label} {value}")

    def WriteResultsLog(self, message):
        print(f"Results log: {message}")

    def ElapsedTime(self, start_time):
        elapsed_time = datetime.datetime.now() - start_time
        return str(elapsed_time)

    def Compare(self, message, expected, actual, options=CompareOptions.None_):
        if expected == actual:
            if options != CompareOptions.SuppressPass:
                print(f"Pass: {message}")
            return TestStatus.Pass
        else:
            print(f"Fail: {message}, Expected: {expected}, Actual: {actual}")
            return TestStatus.FAIL

    def Do(self, message, action, ex=None, suppressPass=False):
        start_time = datetime.datetime.now()
        if not suppressPass:
            self.LogBusy(True, message)

        try:
            action()
            status = TestStatus.Pass
            label = "Time:"
            value = self.ElapsedTime(start_time)
        except Exception as act_ex:
            status = TestStatus.FAIL
            label = "Exception:"
            value = str(act_ex)

        if not suppressPass:
            self.LogBusy(False, message)
            self.LogResult(status, message, label, value)
        elif status != TestStatus.Pass:
            self.LogResult(status, message, label, value)

        return status == TestStatus.Pass

    def DoWithFunc(self, message, func, suppressPass=False):
        return self.Do(message, lambda: func(), suppressPass)

    def DoWithException(self, message, action, expEx, maybe=False, suppressPass=False):
        expStr = "Success" if expEx is None else "Exception"
        options = CompareOptions.SuppressPass if suppressPass else CompareOptions.None_

        if not self.Verbose:
            options |= CompareOptions.SuppressPass

        if not suppressPass:
            self.LogBusy(True, message)

        try:
            action()
            if not suppressPass:
                self.LogBusy(False, message)

            if maybe:
                return True
            else:
                return TestStatus.Pass == self.Compare(message, expStr, "Success", options=options)
        except Exception as act_ex:
            if not suppressPass:
                self.LogBusy(False, message)

            status = self.Compare(message, expStr, "Exception", options=options)

            try:
                if status == TestStatus.Pass and suppressPass:
                    self.BeforeLoggingFailure = lambda: self.WriteResultsLog(
                        f"Pass  {message:<37}  Expect:  Exception  Actual: Exception")
                    self.BeforeLoggingFailure = None

                status |= self.Compare("    Exception type", expEx.__class__.__name__, act_ex.__class__.__name__, options=CompareOptions.SuppressPass)
                status |= self.Compare("    Exception message", str(expEx), str(act_ex), options=CompareOptions.SuppressPass)

                if expEx:
                    checker = None
                    for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
                        if hasattr(method, "_is_exception_checker"):
                            params = inspect.signature(method).parameters
                            if len(params) == 2 and list(params.values())[0].annotation == expEx.__class__:
                                checker = method
                                break

                    if checker:
                        status |= checker(expEx, act_ex)

                return status == TestStatus.Pass
            finally:
                self.BeforeLoggingFailure = None

    def DoWithExceptionMessage(self, message, action, expMsg, maybe=False):
        return self.DoWithException(message, action, Exception(expMsg), maybe)

    def Sleep(self, seconds, message=None):
        fmt = lambda s: str(datetime.timedelta(seconds=s))

        message = message or f"Sleep for {fmt(seconds)}."

        for sec in range(seconds):
            if self.Verbose:
                self.LogProgress(message, "Elapsed:", fmt(sec))
            time.sleep(1)

        if self.Verbose:
            self.LogComplete(message, "Elapsed:", fmt(seconds))





