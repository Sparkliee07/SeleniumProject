from enum import IntEnum
from functools import wraps

class SltPlatform(IntEnum):
    None_ = 0x0000
    Titan = 0x0001
    TitanHP = 0x0002
    Aries = 0x0004
    Mercury = 0x0008
    SaturnHD = 0x0010
    All = 0x00FF

class SubSltPlatform(IntEnum):
    None_ = 0x0
    TitanHP_1 = 0x1  # Cayman TODO: Change name
    TitanScan = 0x2
    All = 0xFF

def test_method(description=None, standalone=False, run_once=False, parallel=False, platform=SltPlatform.All):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.description = description
        wrapper.standalone = standalone
        wrapper.run_once = run_once
        wrapper.parallel = parallel
        wrapper.platform = platform
        return wrapper
    return decorator


@test_method(description="Sample test", standalone=True, run_once=True, parallel=True, platform=SltPlatform.Titan)
def sample_test():
    # Test code here
    print("Sample Test ")
    pass


if __name__ == "__main__":
    sample_test()
