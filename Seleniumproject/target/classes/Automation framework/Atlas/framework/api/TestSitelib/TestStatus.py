from enum import Enum

class TestStatus(Enum):
    None_ = -1
    Pass = 0
    FAIL = 1
    Busy = 2
    TODO = 3
    Skip = 4