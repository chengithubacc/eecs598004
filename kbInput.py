import ctypes
from ctypes import wintypes
import time
from GD2 import Gestures

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12
VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28
VK_BACK = 0x42
VK_CHANGE = 0x43  # 7: pinch, C_key
VK_RESET = 0x52
VK_SPACE = 0x0A
VK_P = 0x50


# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def createKeyInput(val):
    if val == Gestures.NO_GESTURE:
        return
        PressKey(VK_SPACE)
        time.sleep(0.05)
        ReleaseKey(VK_SPACE)

    elif val == Gestures.SWIPE_UP:
        PressKey(VK_UP)
        time.sleep(0.05)
        ReleaseKey(VK_UP)

    elif val == Gestures.SWIPE_DOWN:
        PressKey(VK_DOWN)
        time.sleep(0.05)
        ReleaseKey(VK_DOWN)

    elif val == Gestures.SWIPE_LEFT:
        PressKey(VK_LEFT)
        time.sleep(0.05)
        ReleaseKey(VK_LEFT)

    elif val == Gestures.SWIPE_RIGHT:
        PressKey(VK_RIGHT)
        time.sleep(0.05)
        ReleaseKey(VK_RIGHT)

    elif val == Gestures.THREE_PRESS_HOLD:
        PressKey(VK_BACK)
        time.sleep(0.05)
        ReleaseKey(VK_BACK)

    elif val == Gestures.PINCH:
        PressKey(VK_CHANGE)
        time.sleep(0.05)
        ReleaseKey(VK_CHANGE)

    elif val == Gestures.FOUR_PRESS_HOLD:
        PressKey(VK_RESET)
        time.sleep(0.05)
        ReleaseKey(VK_RESET)


    elif val == Gestures.PALM_PRESSING:
        PressKey(VK_P)
        time.sleep(0.05)
        ReleaseKey(VK_P)

def AltTab():
    """Press Alt+Tab and hold Alt key for 2 seconds
    in order to see the overlay.
    """
    while True:
        PressKey(VK_LEFT)
        time.sleep(0.05)
        ReleaseKey(VK_LEFT)

        PressKey(VK_RIGHT)
        time.sleep(0.05)
        ReleaseKey(VK_RIGHT)

        PressKey(VK_UP)
        time.sleep(0.05)
        ReleaseKey(VK_UP)

        PressKey(VK_DOWN)
        time.sleep(0.05)
        ReleaseKey(VK_DOWN)

    #
    # PressKey(VK_MENU)   # Alt
    # PressKey(VK_TAB)    # Tab
    # ReleaseKey(VK_TAB)  # Tab~
    # time.sleep(1)
    # ReleaseKey(VK_MENU) # Alt~

if __name__ == "__main__":
    AltTab()
    input()