import re
import math
from typing import List, Callable, TypeVar, Optional
from enum import Enum
from ATLAS.framework.api.TestSiteLib.TestStatus import TestStatus
from ATLAS.framework.api.TestSiteLib.CompareOptions import CompareOptions

T = TypeVar('T')

class BaseTest:
    def __init__(self):
        self.BeforeLoggingFailure: Optional[Callable[[], None]] = None

    def Compare(self, message: str, expect: T, actual: T, compare: Optional[Callable[[T, T], bool]] = None,
                options: CompareOptions = CompareOptions.None_, format: str = "") -> TestStatus:
        expStr = "(null)" if expect is None else f"{expect:{format}}"
        actStr = "(null)" if actual is None else f"{actual:{format}}"
        compare = compare or self.CompareEqual
        expLabel = self.ExpectLabel(compare)
        status = TestStatus.Pass if compare(expect, actual) else TestStatus.FAIL
        if status == TestStatus.FAIL and self.BeforeLoggingFailure:
            self.BeforeLoggingFailure()
        self.LogResult(status, message, f"{expLabel}:", expStr, "Actual:", actStr, options)
        return status

    def ExpectLabel(self, compare: Callable[[T, T], bool]) -> str:
        return getattr(compare, 'expect_label', "Expect")

    def CompareEqual(self, expect: T, actual: T) -> bool:
        if expect is not None:
            return expect == actual
        return actual is None

    def CompareEqualFloat(self, expect: float, actual: float) -> bool:
        return expect == actual or (math.isnan(expect) and math.isnan(actual))

    def CompareNot(self, expect: T, actual: T) -> bool:
        if expect is not None:
            return not expect == actual
        return actual is not None

    def CompareApproxInt(self, precision: int) -> Callable[[int, int], bool]:
        return lambda e, a: abs(e - a) <= precision

    def CompareApproxFloat(self, precision: float) -> Callable[[float, float], bool]:
        return lambda e, a: abs(e - a) <= precision

    @staticmethod
    def CompareMin(expect: T, actual: T) -> bool:
        return actual >= expect

    @staticmethod
    def CompareMax(expect: T, actual: T) -> bool:
        return actual <= expect

    @staticmethod
    def CompareLessThan(expect: T, actual: T) -> bool:
        return actual < expect

    @staticmethod
    def CompareGreaterThan(expect: T, actual: T) -> bool:
        return actual > expect

    def CompareRange(self, message: str, min_val: T, max_val: T, actual: T) -> TestStatus:
        status_min = self.Compare(message, min_val, actual, self.CompareMin)
        status_max = self.Compare(message, max_val, actual, self.CompareMax)
        return status_min if status_min == TestStatus.FAIL else status_max

    @staticmethod
    def CompareRegex(expect: str, actual: str) -> bool:
        return re.match(expect, actual) is not None

    def CompareAny(self, message: str, expect: List[T], actual: T,
                   compare: Optional[Callable[[T, T], bool]] = None,
                   options: CompareOptions = CompareOptions.SuppressPass) -> TestStatus:
        actStr = "(null)" if actual is None else str(actual)
        compare = compare or self.CompareEqual
        expLabel = self.ExpectLabel(compare)
        for exp in expect:
            if compare(exp, actual):
                expStr = "(null)" if exp is None else str(exp)
                self.LogResult(TestStatus.Pass, message, f"{expLabel}:", expStr, "Actual:", actStr, options)
                return TestStatus.Pass
        expStr = "(null)" if not expect else ",".join(str(e) for e in expect)
        self.LogResult(TestStatus.FAIL, message, f"{expLabel}:", expStr, "Actual:", actStr)
        return TestStatus.FAIL

    def CompareList(self, message: str, expect: List[T], actual: List[T],
                    compare: Optional[Callable[[str, T, T], TestStatus]] = None,
                    options: CompareOptions = CompareOptions.SuppressPass,
                    maxFail: int = float('inf'), increment: int = 1,
                    indexFormat: str = "{0}") -> TestStatus:
        status = TestStatus.Pass
        if self.CompareNull(message, expect is None, actual):
            return status
        compare = compare or (lambda m, e, a: self.Compare(m, e, a, None))

        failCount = 0
        for ii in range(0, len(expect), increment):
            indexStr = indexFormat.format(ii)
            itemStatus = compare(f"{message}[{indexStr}]", expect[ii], actual[ii])
            status = itemStatus if itemStatus == TestStatus.FAIL else status
            if itemStatus == TestStatus.FAIL and failCount > maxFail:
                self.LogResult(status, message, "Abort:", "Too many failures.")
                return status

        if len(expect) > len(actual):
            status = self.LogResult(TestStatus.FAIL, f"[{len(actual)}]", "Expect:", str(expect[len(actual)]), "Actual:",
                                    "(absent)")

        if len(actual) > len(expect):
            status = self.LogResult(TestStatus.FAIL, f"[{len(expect)}]", "Expect:", "(absent)", "Actual:",
                                    str(actual[len(expect)]))

        return status

    def CompareSet(self, message: str, expect: Set[T], actual: Set[T],
                   compare: Optional[Callable[[T, T], bool]] = None,
                   options: CompareOptions = CompareOptions.None_,
                   maxFail: int = float('inf')) -> TestStatus:

        status = TestStatus.Pass

        if self.CompareNull(message, expect is None, actual):
            return status

        compare = compare or self.CompareEqual

        extra = set(actual)

        if len(expect) == 0 and len(actual) == 0:
            self.Compare(f"{message}", "Empty", "Empty")

        for exp in expect:
            present = any(compare(exp, a) for a in actual)
            status = self.Compare(f"{message} {exp}", "Present", "Present" if present else "Absent", options=options)
            if present:
                extra.remove(exp)

        for act in extra:
            status = self.Compare(f"{message} {act}", "Absent", "Present")

        return status