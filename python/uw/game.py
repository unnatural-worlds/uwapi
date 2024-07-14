import os
import sys
from cffi import FFI
from .helpers import c_str
from .helpers import Severity
from .helpers import ConnectionState
from .helpers import MapState

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
        print(f"api version {self._api.UW_VERSION}")
        self._api.uwInitialize(self._api.UW_VERSION)

        self._log_callback = self._ffi.callback("UwLogCallbackType", self.log_callback)
        self._log_delegate = self._api.uwSetLogCallback(self._log_callback)

        self._update_callback = self._ffi.callback("UwUpdateCallbackType", self.update_callback)
        self._tick_delegate = self._api.uwSetUpdateCallback(self._update_callback)
        print("aa")
        # Interop.uwSetUpdateCallback(UpdateDelegate)

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

    # static void ExceptionCallback([MarshalAs(UnmanagedType.LPStr)] string message)
    # {
    #     Console.WriteLine("exception: " + message);
    #     if (System.Diagnostics.Debugger.IsAttached)
    #         System.Diagnostics.Debugger.Break();
    # }
    #
    def log_callback(self, data):
        # TODO data type
        print(data.severity, self._ffi.string(data.message).decode("utf-8"))




    def update_callback(self, tick: int, stepping: bool):
        self._tick = tick

        # TODO ?!
        #     if (Updating != null)
        #         Updating(null, stepping);
        # }

        # static readonly Interop.UwLogCallbackType LogDelegate = new Interop.UwLogCallbackType(LogCallback);

        #     using GameStateEnum = Interop.UwGameStateEnum;
        #     using ShootingData = Interop.UwShootingData;
        #
        # static readonly Interop.UwExceptionCallbackType ExceptionDelegate = new Interop.UwExceptionCallbackType(ExceptionCallback);

        # static readonly Interop.UwConnectionStateCallbackType ConnectionStateDelegate = new Interop.UwConnectionStateCallbackType(ConnectionStateCallback);
        # static readonly Interop.UwGameStateCallbackType GameStateDelegate = new Interop.UwGameStateCallbackType(GameStateCallback);
        # static readonly Interop.UwMapStateCallbackType MapStateDelegate = new Interop.UwMapStateCallbackType(MapStateCallback);
        # static readonly Interop.UwUpdateCallbackType UpdateDelegate = new Interop.UwUpdateCallbackType(UpdateCallback);
        # static readonly Interop.UwShootingCallbackType ShootingDelegate = new Interop.UwShootingCallbackType(ShootingCallback);

        # static void ExceptionCallback([MarshalAs(UnmanagedType.LPStr)] string message)
        # {
        #     Console.WriteLine("exception: " + message);
        #     if (System.Diagnostics.Debugger.IsAttached)
        #         System.Diagnostics.Debugger.Break();
        # }
        #
        # static void LogCallback(ref Interop.UwLogCallback data)
        # {
        #     Console.WriteLine(Marshal.PtrToStringAnsi(data.message));
        # }
        #
        # static void ConnectionStateCallback(ConnectionStateEnum state)
        # {
        #     Console.WriteLine("connection state: " + state);
        #     if (ConnectionStateChanged != null)
        #         ConnectionStateChanged(null, state);
        # }
        #
        # static void GameStateCallback(GameStateEnum state)
        # {
        #     Console.WriteLine("game state: " + state);
        #     if (GameStateChanged != null)
        #         GameStateChanged(null, state);
        # }
        #
        # static void MapStateCallback(MapStateEnum state)
        # {
        #     Console.WriteLine("map state: " + state);
        #     if (MapStateChanged != null)
        #         MapStateChanged(null, state);
        # }
        #
        # static void UpdateCallback(uint tick, bool stepping)
        # {
        #     Game.tick = tick;
        #     if (Updating != null)
        #         Updating(null, stepping);
        # }
        #
        # static void ShootingCallback(ref ShootingData data)
        # {
        #     if (Shooting != null)
        #         Shooting(null, data);
        # }
        #
        # static Game()
        # {
        #     AppDomain.CurrentDomain.ProcessExit += Destructor;
        #
        #     Interop.uwInitialize(Interop.UW_VERSION);
        #     Interop.uwSetExceptionCallback(ExceptionDelegate);
        #     Interop.uwSetLogCallback(LogDelegate);
        #     Interop.uwSetConnectionStateCallback(ConnectionStateDelegate);
        #     Interop.uwSetGameStateCallback(GameStateDelegate);
        #     Interop.uwSetMapStateCallback(MapStateDelegate);
        #     Interop.uwSetUpdateCallback(UpdateDelegate);
        #     Interop.uwSetShootingCallback(ShootingDelegate, true);
        #
        #     // make sure that others register their callbacks too
        #     Prototypes.All();
        #     Map.Positions();
        #     World.Entities();
        # }
        #
