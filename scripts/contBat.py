# This code is used from https://github.com/Zuzu-Typ/XInput-Python/blob/master/XInput.py
# Kodi doesnt allow the use of third party python packages so a custom script had to be created with
# the package code

import ctypes, ctypes.util

from ctypes import Structure, POINTER

from math import sqrt

import time

from threading import Thread, Lock

import xbmc

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

def XInputGetState(dwUserIndex, state):
    return libXInput.XInputGetState(dwUserIndex, ctypes.byref(state))

libXInput.XInputSetState.argtypes = [DWORD, POINTER(XINPUT_VIBRATION)]
libXInput.XInputSetState.restype = DWORD

def XInputSetState(dwUserIndex, vibration):
    return libXInput.XInputSetState(dwUserIndex, ctypes.byref(vibration))

libXInput.XInputGetBatteryInformation.argtypes = [DWORD, BYTE, POINTER(XINPUT_BATTERY_INFORMATION)]
libXInput.XInputGetBatteryInformation.restype = DWORD

def XInputGetBatteryInformation(dwUserIndex, devType, batteryInformation):
    return libXInput.XInputGetBatteryInformation(dwUserIndex, devType, ctypes.byref(batteryInformation))
#/defining XInput compatible structures #

# defining file-local variables #
_battery_type_dict = {BATTERY_TYPE_DISCONNECTED : "DISCONNECTED",
                      BATTERY_TYPE_WIRED : "WIRED",
                      BATTERY_TYPE_ALKALINE : "ALKALINE",
                      BATTERY_TYPE_NIMH : "NIMH",
                      BATTERY_TYPE_UNKNOWN : "UNKNOWN"}

_battery_level_dict = {BATTERY_LEVEL_EMPTY : "EMPTY",
                       BATTERY_LEVEL_LOW : "LOW",
                       BATTERY_LEVEL_MEDIUM : "MEDIUM",
                       BATTERY_LEVEL_FULL : "FULL"}

_last_states = (State(), State(), State(), State())

_last_norm_values = [None, None, None, None]

_connected = [False, False, False, False]

_last_checked = 0

_deadzones = [{DEADZONE_RIGHT_THUMB : XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE,
               DEADZONE_LEFT_THUMB : XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE,
               DEADZONE_TRIGGER : XINPUT_GAMEPAD_TRIGGER_THRESHOLD},
              {DEADZONE_RIGHT_THUMB : XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE,
               DEADZONE_LEFT_THUMB : XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE,
               DEADZONE_TRIGGER : XINPUT_GAMEPAD_TRIGGER_THRESHOLD},
              {DEADZONE_RIGHT_THUMB : XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE,
               DEADZONE_LEFT_THUMB : XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE,
               DEADZONE_TRIGGER : XINPUT_GAMEPAD_TRIGGER_THRESHOLD},
              {DEADZONE_RIGHT_THUMB : XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE,
               DEADZONE_LEFT_THUMB : XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE,
               DEADZONE_TRIGGER : XINPUT_GAMEPAD_TRIGGER_THRESHOLD}]

_button_dict = {0x0001 : "DPAD_UP",
                0x0002 : "DPAD_DOWN",
                0x0004 : "DPAD_LEFT",
                0x0008 : "DPAD_RIGHT",
                0x0010 : "START",
                0x0020 : "BACK",
                0x0040 : "LEFT_THUMB",
                0x0080 : "RIGHT_THUMB",
                0x0100 : "LEFT_SHOULDER",
                0x0200 : "RIGHT_SHOULDER",
                0x1000 : "A",
                0x2000 : "B",
                0x4000 : "X",
                0x8000 : "Y",
        }
#/defining file-local variables #

# defining custom classes and methods #
class XInputNotConnectedError(Exception):
    pass

class XInputBadArgumentError(ValueError):
    pass

def set_deadzone(dzone, value):
    """Sets the deadzone <dzone> to <value>.
Any raw value retruned by the respective stick or trigger
will be clamped to 0 if it's lower than <value>.
The supported deadzones are:
DEADZONE_RIGHT_THUMB (default value is 8689, max is 32767)
DEADZONE_LEFT_THUMB  (default value is 7849, max is 32767)
DEADZONE_TRIGGER     (default value is 30,   max is 255  )"""
    global XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE, XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE, XINPUT_GAMEPAD_TRIGGER_THRESHOLD
    
    assert dzone >= 0 and dzone <= 2, "invalid deadzone"
    
    if value == DEADZONE_DEFAULT:
        value = 7849 if dzone == DEADZONE_LEFT_THUMB else \
                8689 if dzone == DEADZONE_RIGHT_THUMB else \
                30

    if dzone == DEADZONE_LEFT_THUMB:
        assert value >= 0 and value <= 32767
        if value == DEADZONE_DEFAULT: XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE = 7849
        else: XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE = value

    elif dzone == DEADZONE_RIGHT_THUMB:
        assert value >= 0 and value <= 32767
        if value == DEADZONE_DEFAULT: XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE = 8689
        else: XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE = value

    else:
        assert value >= 0 and value <= 255
        if value == DEADZONE_DEFAULT: XINPUT_GAMEPAD_TRIGGER_THRESHOLD = 30
        else: XINPUT_GAMEPAD_TRIGGER_THRESHOLD = value

def get_connected():
    """get_connected() -> (bool, bool, bool, bool)
Returns wether or not the controller at each index is
connected.
You shouldn't check this too frequently."""
    state = XINPUT_STATE()
    out = [False] * 4
    for i in range(4):
        out[i] = (XInputGetState(i, state) == 0)

    return tuple(out)

def get_state(user_index):
    """get_state(int) -> XINPUT_STATE
Returns the raw state of the controller."""
    state = XINPUT_STATE()
    res = XInputGetState(user_index, state)
    if res == ERROR_DEVICE_NOT_CONNECTED:
        raise XInputNotConnectedError("Controller [{}] appears to be disconnected.".format(user_index))

    if res == ERROR_BAD_ARGUMENTS:
        raise XInputBadArgumentError("Controller [{}] doesn't exist. IDs range from 0 to 3.".format(user_index))
    
    assert res == 0, "Couldn't get the state of controller [{}]. Is it disconnected?".format(user_index)

    return state

def get_battery_information(user_index):
    """get_battery_information(int) -> (str, str)
Returns the battery information for controller <user_index>.
The return value is formatted as (<battery_type>, <battery_level>)"""
    battery_information = XINPUT_BATTERY_INFORMATION()
    XInputGetBatteryInformation(user_index, BATTERY_DEVTYPE_GAMEPAD, battery_information)
    return (_battery_type_dict[battery_information.BatteryType], _battery_level_dict[battery_information.BatteryLevel])

def set_vibration(user_index, left_speed, right_speed):
    """Sets the vibration motor speed for controller <user_index>.
The speed ranges from 0.0 to 1.0 (float values) or
0 to 65535 (int values)."""
    if type(left_speed) == float and left_speed <= 1.0:
        left_speed = (round(65535 * left_speed, 0))

    if type(right_speed) == float and right_speed <= 1.0:
        right_speed = (round(65535 * right_speed, 0))
        
    vibration = XINPUT_VIBRATION()
    
    vibration.wLeftMotorSpeed = int(left_speed)
    vibration.wRightMotorSpeed = int(right_speed)

    return XInputSetState(user_index, vibration) == 0

def get_button_values(state):
    """get_button_values(XINPUT_STATE) -> dict
Returns a dict with string keys and boolean values,
representing the button and it's value respectively.
You can get the required state using get_state()"""
    wButtons = state.Gamepad.wButtons
    return {"DPAD_UP" : bool(wButtons & 0x0001),
            "DPAD_DOWN" : bool(wButtons & 0x0002),
            "DPAD_LEFT" : bool(wButtons & 0x0004),
            "DPAD_RIGHT" : bool(wButtons & 0x0008),
            "START" : bool(wButtons & 0x0010),
            "BACK" : bool(wButtons & 0x0020),
            "LEFT_THUMB" : bool(wButtons & 0x0040),
            "RIGHT_THUMB" : bool(wButtons & 0x0080),
            "LEFT_SHOULDER" : bool(wButtons & 0x0100),
            "RIGHT_SHOULDER" : bool(wButtons & 0x0200),
            "A" : bool(wButtons & 0x1000),
            "B" : bool(wButtons & 0x2000),
            "X" : bool(wButtons & 0x4000),
            "Y" : bool(wButtons & 0x8000),
        }

def get_trigger_values(state):
    """get_trigger_values(XINPUT_STATE) -> (float, float)
Returns the normalized left and right trigger values.
You can get the required state using get_state()"""
    LT = state.Gamepad.bLeftTrigger
    RT = state.Gamepad.bRightTrigger

    normLT = 0
    normRT = 0

    if LT > XINPUT_GAMEPAD_TRIGGER_THRESHOLD:
        LT -= XINPUT_GAMEPAD_TRIGGER_THRESHOLD
        normLT = LT / (255. - XINPUT_GAMEPAD_TRIGGER_THRESHOLD)
    else:
        LT = 0

    if RT > XINPUT_GAMEPAD_TRIGGER_THRESHOLD:
        RT -= XINPUT_GAMEPAD_TRIGGER_THRESHOLD
        normRT = RT / (255. - XINPUT_GAMEPAD_TRIGGER_THRESHOLD)
    else:
        RT = 0

    return (normLT, normRT)

def get_thumb_values(state):
    """get_thumb_values(XINPUT_STATE) -> ((float, float), (float, float))
Returns the normalized left and right thumb stick values,
represented as X and Y values.
You can get the required state using get_state()"""
    LX = state.Gamepad.sThumbLX
    LY = state.Gamepad.sThumbLY
    RX = state.Gamepad.sThumbRX
    RY = state.Gamepad.sThumbRY

    magL = sqrt(LX*LX + LY*LY)
    magR = sqrt(RX*RX + RY*RY)

    if magL != 0:
        normLX = LX / magL
        normLY = LY / magL
    else: # if magL == 0 the stick is centered, there is no direction
        normLX = 0
        normLY = 0
    
    if magR != 0:
        normRX = RX / magR
        normRY = RY / magR
    else: # if magR == 0 the stick is centered, there is no direction
        normRX = 0
        normRY = 0


    normMagL = 0
    normMagR = 0

    if (magL > XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE):
        magL = min(32767, magL)

        magL -= XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE

        normMagL = magL / (32767. - XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE)
    else:
        magL = 0

    if (magR > XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE):
        magR = min(32767, magR)

        magR -= XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE

        normMagR = magR / (32767. - XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE)
    else:
        magR = 0

    return ((normLX * normMagL, normLY * normMagL), (normRX * normMagR, normRY * normMagR))


def controller(argument):
    time.sleep(1)
    arg = argument - 1
    cont_connections = get_connected()
    xbmc.executebuiltin('Skin.SetString(controller{}, {})'.format(argument,cont_connections[arg]))
    xbmc.executebuiltin('Skin.SetString(controller{}batcon, {})'.format(argument,""))
    if get_battery_information(arg)[0] == "WIRED":    
        xbmc.executebuiltin('Skin.SetString(controller{}bat, {})'.format(argument,get_battery_information(arg)[0]))
    else:
        xbmc.executebuiltin('Skin.SetString(controller{}bat, {})'.format(argument,get_battery_information(arg)[1]))
    if get_battery_information(arg)[1] == "EMPTY":
        if not cont_connections[arg]:
            xbmc.executebuiltin('Skin.SetString(controller{}batnum, {})'.format(argument,"Not Connected"))
            xbmc.executebuiltin('Skin.SetString(controller{}batcon, {})'.format(argument,"Not Connected"))
        else:
            xbmc.executebuiltin('Skin.SetString(controller{}batnum, {})'.format(argument,"0 %"))
    elif get_battery_information(arg)[1] == "LOW":
        xbmc.executebuiltin('Skin.SetString(controller{}batnum, {})'.format(argument,"15 %"))
        xbmc.executebuiltin('Skin.SetString(snapico,EMPTY.png)') 
        xbmc.executebuiltin('Notification(Battery Low,Please charge controller {} ,2000)'.format(argument))
    elif get_battery_information(arg)[1] == "MEDIUM":
        xbmc.executebuiltin('Skin.SetString(controller{}batnum, {})'.format(argument,"56 %"))
    elif get_battery_information(arg)[1] == "FULL":
        xbmc.executebuiltin('Skin.SetString(controller{}batnum, {})'.format(argument,"100 %"))

controller(1)
controller(2)
controller(3)
controller(4)
