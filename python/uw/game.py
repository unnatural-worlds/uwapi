import os
import sys
from cffi import FFI
from typing import Callable
from typing import List

from .helpers import c_str
from .helpers import Severity
from .helpers import ConnectionState
from .helpers import MapState
from .helpers import LogCallback
from .helpers import GameState
from .helpers import ShootingData

LIB_NAME_PATTERN = "libunnatural-uwapi{}.{}"


def get_lib_name(hardened=False):
    return LIB_NAME_PATTERN.format("-hard" if hardened else "", "dll" if sys.platform == "win32" else "so")


class Game:
    def __init__(self, steam_path: str = "", hardened: bool = False):
        # TODO automated search for the install path in common locations
        # TODO load from env
        api_def = open(os.path.join(os.path.split(os.path.abspath(__file__))[0], "bots.h"), "r").read()
        os.chdir(steam_path)
        self._ffi = FFI()
        self._ffi.cdef(api_def)
        self._api = self._ffi.dlopen(os.path.join(steam_path, get_lib_name(hardened=hardened)))
        # print(f"api version {self._api.UW_VERSION}")
        self._api.uwInitialize(self._api.UW_VERSION)

        self._connection_state_changed_handler = None
        self._updating_handler = None
        self._game_state_changed_handler = None
        self._map_state_changed_handler = None
        self._shooting_handler = None

        self._exception_delegate = self._ffi.callback("UwExceptionCallbackType", self._exception_callback)
        self._exception_callback_func = self._api.uwSetExceptionCallback(self._exception_delegate)

        self._log_delegate = self._ffi.callback("UwLogCallbackType", self._log_callback)
        self._log_callback_func = self._api.uwSetLogCallback(self._log_delegate)

        self._connection_state_delegate = self._ffi.callback("UwConnectionStateCallbackType",
                                                             self._connection_state_callback)
        self._connection_state_callback = self._api.uwSetConnectionStateCallback(self._connection_state_delegate)

        self._game_state_delegate = self._ffi.callback("UwGameStateCallbackType", self._game_state_callback)
        self._game_state_callback_func = self._api.uwSetGameStateCallback(self._game_state_delegate)

        self._map_state_delegate = self._ffi.callback("UwMapStateCallbackType", self._map_state_callback)
        self._map_state_callback_func = self._api.uwSetMapStateCallback(self._map_state_delegate)

        self._update_delegate = self._ffi.callback("UwUpdateCallbackType", self._update_callback)
        self._update_callback_func = self._api.uwSetUpdateCallback(self._update_delegate)

        self._shooting_delegate = self._ffi.callback("UwShootingCallbackType", self._shooting_callback)
        self._shooting_callback_func = self._api.uwSetShootingCallback(self._shooting_delegate)

        # TODO
        #     // make sure that others register their callbacks too
        #     Prototypes.All();
        #     Map.Positions();
        #     World.Entities();

        self._tick = 0

    def __del__(self):
        self._api.uwDeinitialize()

    def log(self, message: str, severity: Severity = Severity.Info):
        self._api.uwLog(severity.value, c_str(message))

    def set_player_name(self, name: str):
        self._api.uwSetPlayerName(c_str(name))

    def set_player_color(self, r: float, g: float, b: float):
        self._api.uwSetPlayerColor(r, g, b)

    def set_start_gui(self, start_gui: bool, extra_params: str = ""):
        self._api.uwSetConnectStartGui(start_gui, c_str(extra_params))

    def set_connect_find_lan(self, timeout_ms: int = 1000000):
        self._api.uwConnectFindLan(timeout_ms)

    def connect_direct(self, address: str, port: int):
        self._api.uwConnectDirect(c_str(address), port)

    def connect_lobby_id(self, lobby_id: int):
        self._api.uwConnectLobbyId(lobby_id)

    def connect_new_server(self, extra_params: str = ""):
        self._api.uwConnectNewServer(c_str(extra_params))

    def disconnect(self):
        self._api.uwDisconnect()

    def connection_state_enum(self) -> ConnectionState:
        return ConnectionState(self._api.uwConnectionState())

    def map_state_enum(self) -> MapState:
        return MapState(self._api.uwMapState())

    def tick(self) -> int:
        return self._tick

    def _exception_callback(self, message):
        print(f"Exception: {self._str(message)}")

    def _log_callback(self, data):
        log_data = LogCallback(self._str(data.message), self._str(data.component), data.severity)
        print(f"{log_data.component}\t{log_data.severity}\t{log_data.message}")

    def set_connection_state_callback(self, callback: Callable[[ConnectionState], None]):
        self._connection_state_changed_handler = callback

    def _connection_state_callback(self, state):
        connection_state = ConnectionState(state)
        print(f"Connection state: {connection_state}")
        if self._connection_state_changed_handler:
            self._connection_state_changed_handler(connection_state)

    def set_game_state_callback(self, callback: Callable[[GameState], None]):
        self._game_state_changed_handler = callback

    def _game_state_callback(self, state):
        game_state = GameState(state)
        print(f"Game state: {game_state}")
        if self._game_state_changed_handler:
            self._game_state_changed_handler(game_state)

    def set_map_state_callback(self, callback: Callable[[MapState], None]):
        self._game_state_changed_handler = callback

    def _map_state_callback(self, state):
        map_state = MapState(state)
        print(f"Map state: {map_state}")
        if self._map_state_changed_handler:
            self._map_state_changed_handler(map_state)

    def set_update_callback(self, callback: Callable[[bool], None]):
        self._updating_handler = callback

    def _update_callback(self, tick: int, stepping: bool):
        self._tick = tick
        if self._updating_handler:
            self._updating_handler(stepping)

    def set_shooting_callback(self, callback: Callable[[List[ShootingData]], None]):
        self._shooting_handler = callback

    def _shooting_callback(self, shoot_data):
        # TODO this probably needs ffi.unpack to extract the array
        shooting_data = ShootingData(shoot_data)
        if self._shooting_handler:
            self._shooting_handler(shooting_data)

    def _str(self, s) -> str:
        return self._ffi.string(s).decode("utf-8")
