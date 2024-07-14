from enum import Enum


def c_str(s: str) -> bytes:
    return bytes(s, encoding="utf-8")


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


