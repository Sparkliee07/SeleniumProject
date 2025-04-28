from enum import IntFlag
from enum import Flag, auto

class CompareOptions(IntFlag):
    None_ = 0
    SuppressPass = 1
    HighlightDiffs = 2
    PrintWide = 4
    AlwaysLog = 8


# class CompareOptions(Flag):
#     None_ = 0
#     SuppressPass = auto()
#     HighlightDiffs = auto()
#     PrintWide = auto()
#     AlwaysLog = auto()

if __name__ == "__main__":
    # Example usage
    print(CompareOptions.None_)
    print(CompareOptions.SuppressPass)
    print(CompareOptions.HighlightDiffs)
    print(CompareOptions.PrintWide)
    print(CompareOptions.AlwaysLog)