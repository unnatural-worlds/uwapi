from enum import Enum


def c_str(s: str) -> bytes:
    return bytes(s, encoding="utf-8")


class LogCallback:
    def __init__(self, message, component, severity):
        self.message = message
        self.component = component
        self.severity = Severity(severity)


class Severity(Enum):
    Note = 0
    Hint = 1
    Warning = 2
    Info = 3
    Error = 4
    Critical = 5


class ConnectionState(Enum):
    NONE = 0
    Connecting = 1
    Connected = 2
    Disconnecting = 3
    Error = 4


class MapState(Enum):
    NONE = 0
    Downloading = 1
    Loading = 2
    Loaded = 3
    Unloading = 4
    Error = 5


class GameState(Enum):
    NONE = 0
    Session = 1
    Preparation = 2
    Game = 3
    Finish = 4


class ShootingUnit:
    def __init__(self, data):
        self.position = data.position
        self.force = data.force
        self.prototype = data.prototype
        self.id = data.id


class ShootingData:
    # TODO is this wrapper useful?
    def __init__(self, data):
        self.shooter = ShootingUnit(data.shooter)
        self.target = ShootingUnit(data.target)

#
#         public struct UwShootingArray
#         {
#             public IntPtr data;
#             public uint count;
#         }
