import os
import sys
from cffi import FFI
from .helpers import c_str

LIB_NAME_PATTERN = "libunnatural-uwapi{}.{}"


def get_lib_name(hardened=False):
    return LIB_NAME_PATTERN.format("-hard" if hardened else "", "dll" if sys.platform == "win32" else "so")


class Game:
    def __init__(self, steam_path: str = "", hardened: bool = False):
        # TODO automated search for the install path in common locations
        api_def = open(os.path.join(os.path.split(os.path.abspath(__file__))[0], "bots.h"), "r").read()
        os.chdir(steam_path)
        ffi = FFI()
        ffi.cdef(api_def)
        self.api = ffi.dlopen(os.path.join(steam_path, get_lib_name(hardened=hardened)))
        self.api.uwInitialize(self.api.UW_VERSION)

    def log(self, message: str, severity=None):
        # TODO
        if severity is None:
            severity = self.api.UwSeverityEnum_Info
        self.api.uwLog(severity, c_str(message))

    def set_player_name(self, name: str):
        self.api.uwSetPlayerName(c_str(name))
