import ctypes, ctypes.util

from ctypes import Structure, POINTER

from math import sqrt

import time

from threading import Thread, Lock


# loading the DLL #
XINPUT_DLL_NAMES = (
    "XInput1_4.dll",
    "XInput9_1_0.dll",
    "XInput1_3.dll",
    "XInput1_2.dll",
    "XInput1_1.dll"
)

libXInput = None

for name in XINPUT_DLL_NAMES:
    found = ctypes.util.find_library(name)
    if found:
        libXInput = ctypes.WinDLL(found)
        break

if not libXInput:
    raise IOError("XInput library was not found.")

#/loading the DLL #

# defining static global variables #
WORD    = ctypes.c_ushort
BYTE    = ctypes.c_ubyte
SHORT   = ctypes.c_short
DWORD   = ctypes.c_ulong

ERROR_SUCCESS               = 0
ERROR_BAD_ARGUMENTS         = 160
ERROR_DEVICE_NOT_CONNECTED  = 1167

XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE  = 7849
XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE = 8689
XINPUT_GAMEPAD_TRIGGER_THRESHOLD    = 30

BATTERY_DEVTYPE_GAMEPAD         = 0x00
BATTERY_TYPE_DISCONNECTED       = 0x00
BATTERY_TYPE_WIRED              = 0x01
BATTERY_TYPE_ALKALINE           = 0x02
BATTERY_TYPE_NIMH               = 0x03
BATTERY_TYPE_UNKNOWN            = 0xFF
BATTERY_LEVEL_EMPTY             = 0x00
BATTERY_LEVEL_LOW               = 0x01
BATTERY_LEVEL_MEDIUM            = 0x02
BATTERY_LEVEL_FULL              = 0x03

BUTTON_DPAD_UP                  = 0x000001
BUTTON_DPAD_DOWN                = 0x000002
BUTTON_DPAD_LEFT                = 0x000004
BUTTON_DPAD_RIGHT               = 0x000008
BUTTON_START                    = 0x000010
BUTTON_BACK                     = 0x000020
BUTTON_LEFT_THUMB               = 0x000040
BUTTON_RIGHT_THUMB              = 0x000080
BUTTON_LEFT_SHOULDER            = 0x000100
BUTTON_RIGHT_SHOULDER           = 0x000200
BUTTON_A                        = 0x001000
BUTTON_B                        = 0x002000
BUTTON_X                        = 0x004000
BUTTON_Y                        = 0x008000

STICK_LEFT                      = 0x010000
STICK_RIGHT                     = 0x020000
TRIGGER_LEFT                    = 0x040000
TRIGGER_RIGHT                   = 0x080000

FILTER_PRESSED_ONLY                = 0x100000
FILTER_RELEASED_ONLY                  = 0x200000
FILTER_NONE                     = 0xffffff-FILTER_PRESSED_ONLY-FILTER_RELEASED_ONLY

DEADZONE_LEFT_THUMB             = 0
DEADZONE_RIGHT_THUMB            = 1
DEADZONE_TRIGGER                = 2

DEADZONE_DEFAULT                = -1

EVENT_CONNECTED         = 1
EVENT_DISCONNECTED      = 2
EVENT_BUTTON_PRESSED    = 3
EVENT_BUTTON_RELEASED   = 4
EVENT_TRIGGER_MOVED     = 5
EVENT_STICK_MOVED       = 6

LEFT    = 0
RIGHT   = 1
#/defining static global variables #

# defining XInput compatible structures #
class XINPUT_GAMEPAD(Structure):
    _fields_ = [("wButtons", WORD),
                ("bLeftTrigger", BYTE),
                ("bRightTrigger", BYTE),
                ("sThumbLX", SHORT),
                ("sThumbLY", SHORT),
                ("sThumbRX", SHORT),
                ("sThumbRY", SHORT),
                ]

class XINPUT_STATE(Structure):
    _fields_ = [("dwPacketNumber", DWORD),
                ("Gamepad", XINPUT_GAMEPAD),
                ]

State = XINPUT_STATE

class XINPUT_VIBRATION(Structure):
    _fields_ = [("wLeftMotorSpeed", WORD),
                ("wRightMotorSpeed", WORD),
                ]

class XINPUT_BATTERY_INFORMATION(Structure):
    _fields_ = [("BatteryType", BYTE),
                ("BatteryLevel", BYTE),
                ]

libXInput.XInputGetState.argtypes = [DWORD, POINTER(XINPUT_STATE)]
libXInput.XInputGetState.restype = DWORD

def XInputGetBatteryInformation(dwUserIndex, devType, batteryInformation):
    return libXInput.XInputGetBatteryInformation(dwUserIndex, devType, ctypes.byref(batteryInformation))

print(XINPUT_BATTERY_INFORMATION(0,0))