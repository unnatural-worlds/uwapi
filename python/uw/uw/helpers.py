from enum import Enum
from typing import List
from typing import Any


def _c_str(s: str) -> bytes:
    return bytes(s, encoding="utf-8")


def _to_str(ffi, s) -> str:
    return ffi.string(s).decode("utf-8")


def _unpack_list(ffi, data) -> List[Any]:
    if data.count > 0:
        return ffi.unpack(data.ids, data.count)
    return []


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


class OrderType(Enum):
    NONE = 0
    Stop = 1
    Guard = 2
    Run = 3
    Fight = 4
    Load = 5
    Unload = 6
    SelfDestruct = 7


class OrderPriority(Enum):
    NONE = 0
    Assistant = 1 << 0
    User = 1 << 1
    Enqueue = 1 << 2
    Repeat = 1 << 3


class Prototype(Enum):
    NONE = 0
    Resource = 1
    Recipe = 2
    Construction = 3
    Unit = 4


class OverviewFlags(Enum):
    NONE = 0
    Resource = 1 << 0
    Construction = 1 << 1
    MobileUnit = 1 << 2
    StaticUnit = 1 << 3
    Unit = (1 << 2) | (1 << 3)


class LogCallback:
    def __init__(self, message: str, component: str, severity: Severity):
        self.message = message
        self.component = component
        self.severity = severity

    @staticmethod
    def from_c(ffi, data):
        return LogCallback(_to_str(ffi, data.message), _to_str(ffi, data.component), Severity(data.severity))


class Order:
    def __init__(self, entity: int, position: int, order_type: OrderType, priority: OrderPriority):
        self.entity = entity
        self.position = position
        self.order_type = order_type
        self.priority = priority

    @staticmethod
    def from_c(data):
        return Order(data.entity, data.position, OrderType(data.order_type), OrderPriority(data.priority))


class ShootingUnit:
    def __init__(self, data):
        self.position = data.position
        self.force = data.force
        self.prototype = data.prototype
        self.id = data.id

    @staticmethod
    def _from_c(self, data):
        self.position = data.position
        self.force = data.force
        self.prototype = data.prototype
        self.id = data.id


class ShootingData:
    def __init__(self, shooter: ShootingUnit, target: ShootingUnit):
        self.shooter = shooter
        self.target = target

    @staticmethod
    def from_c(data):
        return ShootingData(ShootingUnit(data.shooter), ShootingUnit(data.target))
