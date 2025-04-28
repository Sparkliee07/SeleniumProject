from ctypes import *
import enum

class NETRESOURCE(Structure):
    _fields_ = [
        ("dwScope", c_int),
        ("dwType", c_int),
        ("dwDisplayType", c_int),
        ("dwUsage", c_int),
        ("lpLocalName", c_wchar_p),
        ("lpRemoteName", c_wchar_p),
        ("lpComment", c_wchar_p),
        ("lpProvider", c_wchar_p),
    ]

class Result(enum.Enum):
    NO_ERROR = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_ALREADY_ASSIGNED = 85
    ERROR_BAD_DEVICE = 1200
    ERROR_BAD_NET_NAME = 67
    ERROR_BAD_PROVIDER = 1204
    ERROR_CANCELLED = 1223
    ERROR_EXTENDED_ERROR = 1208
    ERROR_INVALID_ADDRESS = 487
    ERROR_INVALID_PARAMETER = 87
    ERROR_INVALID_PASSWORD = 1216
    ERROR_MORE_DATA = 234
    ERROR_NO_MORE_ITEMS = 259
    ERROR_NO_NET_OR_BAD_PATH = 1203
    ERROR_SESSION_CREDENTIAL_CONFLICT = 1219
    ERROR_NO_NETWORK = 1222
    ERROR_BAD_PROFILE = 1206
    ERROR_CANNOT_OPEN_PROFILE = 1205
    ERROR_DEVICE_IN_USE = 2404
    ERROR_NOT_CONNECTED = 2250
    ERROR_OPEN_FILES = 2401

RESOURCETYPE_DISK = 0x00000001

mpr = WinDLL('Mpr.dll')

WNetUseConnection = mpr.WNetUseConnectionW
WNetUseConnection.argtypes = [c_void_p, POINTER(NETRESOURCE), c_wchar_p, c_wchar_p, c_int, c_wchar_p, c_void_p, c_void_p]
WNetUseConnection.restype = c_int
