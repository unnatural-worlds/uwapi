import os
import sys

from cffi import FFI
from typing import Callable

from .commands import Commands
from .helpers import _c_str
from .helpers import _to_str
from .helpers import Severity
from .helpers import ConnectionState
from .helpers import MapState
from .helpers import LogCallback
from .helpers import GameState
from .helpers import ShootingData
from .prototypes import Prototypes
from .map import Map
from .world import World
from .helpers import _unpack_list


def get_lib_name(hardened: bool):
    return "{}unnatural-uwapi{}.{}".format(
        "" if sys.platform == "win32" else "lib",
        "-hard" if hardened else "",
        "dll" if sys.platform == "win32" else "so",
    )


def get_default_steam_location():
    if sys.platform == "win32":
        return "C:/Program Files (x86)/Steam/steamapps/common/Unnatural Worlds/bin"
    return "~/.steam/steam/steamapps/common/Unnatural Worlds/bin"


def get_steam_path(steam_path: str) -> str:
    if steam_path != "":
        return steam_path
    steam_path = os.environ.get("UNNATURAL_ROOT", "")
    if steam_path != "":
        return steam_path
    return get_default_steam_location()


class Game:
    def __init__(self, steam_path: str = "", hardened: bool = True):
        api_def = open(
            os.path.join(os.path.split(os.path.abspath(__file__))[0], "bots.h"), "r"
        ).read()

        steam_path = os.path.expanduser(get_steam_path(steam_path))
        print("looking for uw library in: " + steam_path, flush=True)
        os.chdir(steam_path)

        self._ffi = FFI()
        self._ffi.cdef(api_def)
        self._api = self._ffi.dlopen(
            os.path.join(steam_path, get_lib_name(hardened=hardened))
        )
        self._api.uwInitialize(self._api.UW_VERSION)

        self._connection_state_changed_handler = []
        self._game_state_changed_handler = []
        self._map_state_changed_handler = []
        self._updating_handler = []
        self._shooting_handler = []

        self._exception_delegate = self._ffi.callback(
            "UwExceptionCallbackType", self._exception_callback
        )
        self._exception_callback_func = self._api.uwSetExceptionCallback(
            self._exception_delegate
        )

        self._log_delegate = self._ffi.callback("UwLogCallbackType", self._log_callback)
        self._log_callback_func = self._api.uwSetLogCallback(self._log_delegate)

        self._connection_state_delegate = self._ffi.callback(
            "UwConnectionStateCallbackType", self._connection_state_callback
        )
        self._connection_state_callback_func = self._api.uwSetConnectionStateCallback(
            self._connection_state_delegate
        )

        self._game_state_delegate = self._ffi.callback(
            "UwGameStateCallbackType", self._game_state_callback
        )
        self._game_state_callback_func = self._api.uwSetGameStateCallback(
            self._game_state_delegate
        )

        self._map_state_delegate = self._ffi.callback(
            "UwMapStateCallbackType", self._map_state_callback
        )
        self._map_state_callback_func = self._api.uwSetMapStateCallback(
            self._map_state_delegate
        )

        self._update_delegate = self._ffi.callback(
            "UwUpdateCallbackType", self._update_callback
        )
        self._update_callback_func = self._api.uwSetUpdateCallback(
            self._update_delegate
        )

        self._shooting_delegate = self._ffi.callback(
            "UwShootingCallbackType", self._shooting_callback
        )
        self._shooting_callback_func = self._api.uwSetShootingCallback(
            self._shooting_delegate
        )

        self._tick = 0

        self.prototypes = Prototypes(self._api, self._ffi, self)
        self.map = Map(self._api, self._ffi, self)
        self.world = World(self._api, self._ffi, self)
        self.commands = Commands(self._api, self._ffi)

    def __del__(self):
        self._api.uwDeinitialize()

    def log(self, message: str, severity: Severity = Severity.Info):
        self._api.uwLog(severity.value, _c_str(message))

    def log_info(self, message: str):
        self.log(message, Severity.Info)

    def log_warning(self, message: str):
        self.log(message, Severity.Warning)

    def log_error(self, message: str):
        self.log(message, Severity.Error)

    def set_player_name(self, name: str):
        self._api.uwSetPlayerName(_c_str(name))

    def set_player_color(self, r: float, g: float, b: float):
        self._api.uwSetPlayerColor(r, g, b)

    def set_start_gui(self, start_gui: bool, extra_params: str = "--observer 1"):
        self._api.uwSetConnectStartGui(start_gui, _c_str(extra_params))

    def connect_find_lan(self, timeout_us: int = 1000000) -> bool:
        return self._api.uwConnectFindLan(timeout_us)

    def connect_direct(self, address: str, port: int):
        self._api.uwConnectDirect(_c_str(address), port)

    def connect_lobby_id(self, lobby_id: int):
        self._api.uwConnectLobbyId(lobby_id)

    def connect_new_server(
            self, visibility: int = 0, name: str = "", extra_params: str = ""
    ):
        self._api.uwConnectNewServer(visibility, _c_str(name), _c_str(extra_params))

    def try_reconnect(self) -> bool:
        return self._api.uwTryReconnect()

    def disconnect(self):
        self._api.uwDisconnect()

    def connection_state(self) -> ConnectionState:
        return ConnectionState(self._api.uwConnectionState())

    def game_state(self) -> GameState:
        return GameState(self._api.uwGameState())

    def map_state(self) -> MapState:
        return MapState(self._api.uwMapState())

    def tick(self) -> int:
        return self._tick

    def _exception_callback(self, message):
        print(f"Exception: {_to_str(self._ffi, message)}", flush=True)
        breakpoint()

    def _log_callback(self, data):
        log_data = LogCallback.from_c(self._ffi, data)
        print(log_data.message, flush=True)

    def add_connection_state_callback(
            self, callback: Callable[[ConnectionState], None]
    ):
        self._connection_state_changed_handler.append(callback)

    def _connection_state_callback(self, state):
        connection_state = ConnectionState(state)
        for eh in self._connection_state_changed_handler:
            eh(connection_state)

    def add_game_state_callback(self, callback: Callable[[GameState], None]):
        self._game_state_changed_handler.append(callback)

    def _game_state_callback(self, state):
        game_state = GameState(state)
        for eh in self._game_state_changed_handler:
            eh(game_state)

    def add_map_state_callback(self, callback: Callable[[MapState], None]):
        self._map_state_changed_handler.append(callback)

    def _map_state_callback(self, state):
        map_state = MapState(state)
        for eh in self._map_state_changed_handler:
            eh(map_state)

    def add_update_callback(self, callback: Callable[[bool], None]):
        self._updating_handler.append(callback)

    def _update_callback(self, tick: int, stepping: bool):
        self._tick = tick
        for eh in self._updating_handler:
            eh(stepping)

    def add_shooting_callback(self, callback: Callable[[list[ShootingData]], None]):
        self._shooting_handler.append(callback)

    def _shooting_callback(self, shoot_data):
        if not self._shooting_handler:
            return
        shooting_data = [
            ShootingData.from_c(i) for i in _unpack_list(self._ffi, shoot_data, "data")
        ]
        for eh in self._shooting_handler:
            eh(shooting_data)
