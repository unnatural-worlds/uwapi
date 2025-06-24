import json
from dataclasses import dataclass, field
from typing import Dict, Any
from .interop import *
from .events import uw_events

@dataclass
class Prototype:
    id: int = 0
    type: UwPrototypeTypeEnum = UwPrototypeTypeEnum.Nothing
    name: str = ""
    data: Dict[str, Any] = field(default_factory=dict)

class Prototypes:
    _instance = None
    _all: Dict[int, Prototype] = {}
    _definitions: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            uw_events.on_map_state(cls._instance._map_state)
        return cls._instance

    def get(self, id: int) -> Prototype:
        return self._all[id]

    def type(self, id: int) -> UwPrototypeTypeEnum:
        p = self._all.get(id, None)
        if p is not None:
            return p.type
        return UwPrototypeTypeEnum.Nothing

    def _load(self) -> None:
        uw_interop.uwLog(UwSeverityEnum.Info, "loading prototypes")
        self._all: Dict[int, Prototype] = {}
        self._definitions: Dict[str, Any] = {}
        for id in uw_interop.uwAllPrototypes().ids:
            p = Prototype(id)
            p.type = uw_interop.uwPrototypeType(id)
            p.data = json.loads(uw_interop.uwPrototypeJson(id))
            p.name = p.data["name"]
            self._all[id] = p
        self._definitions = json.loads(uw_interop.uwDefinitionsJson())
        uw_interop.uwLog(UwSeverityEnum.Info, "prototypes loaded")

    def _map_state(self, state: UwMapStateEnum) -> None:
        if state == UwMapStateEnum.Loaded:
            self._load()

uw_prototypes = Prototypes()
