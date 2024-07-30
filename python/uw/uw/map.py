import math

from .helpers import MapState
from .helpers import OverviewFlags


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class Map:
    def __init__(self, api, ffi, game):
        self._api = api
        self._ffi = ffi
        self._game = game

        self._game.add_map_state_callback(self._map_state_changed)
        self._game.add_update_callback(self._updating)

        self._name: str = ""
        self._guid: str = ""
        self._path: str = ""
        self._max_players: int = 0
        self._positions: list[Vector3] = []
        self._ups: list[Vector3] = []
        self._neighbors: list[list[int]] = []
        self._terrains: list[bytes] = []
        self._overview: list[OverviewFlags] = []

    def name(self) -> str:
        return self._name

    def guid(self) -> str:
        return self._guid

    def path(self) -> str:
        return self._path

    def max_players(self) -> int:
        return self._max_players

    def positions(self) -> list[Vector3]:
        return self._positions

    def ups(self) -> list[Vector3]:
        return self._ups

    def neighbors(self) -> list[list[int]]:
        return self._neighbors

    def neighbors_on_pos(self, pos: int) -> list[int]:
        return self._neighbors[pos]

    def terrains(self) -> list[bytes]:
        return self._terrains

    def overview(self) -> list[OverviewFlags]:
        return self._overview

    def entities(self, position: int) -> list[int]:
        ns = self._ffi.new("struct UwIds *")
        self._api.uwOverviewIds(position, ns)
        return self._ffi.unpack(ns)

    def area_range(self, point: Vector3, radius: float) -> list[int]:
        tiles = self._ffi.new("struct UwIds *")
        self._api.uwAreaRange(point.x, point.y, point.z, radius, tiles)
        return self._ffi.unpack(tiles)

    def area_connected(self, position: int, radius: float) -> list[int]:
        tiles = self._ffi.new("struct UwIds *")
        self._api.uwAreaConnected(position, radius, tiles)
        return self._ffi.unpack(tiles)

    def area_neighborhood(self, position: int, radius: float) -> list[int]:
        tiles = self._ffi.new("struct UwIds *")
        self._api.uwAreaNeighborhood(position, radius, tiles)
        return self._ffi.unpack(tiles)

    def area_extended(self, position: int, radius: float) -> list[int]:
        tiles = self._ffi.new("struct UwIds *")
        self._api.uwAreaExtended(position, radius, tiles)
        return self._ffi.unpack(tiles)

    def test_visible(self, a: Vector3, b: Vector3) -> bool:
        return self._ffi.uwTestVisible(a.x, a.y, a.z, b.x, b.y, b.z)

    def test_shooting(self, shooter_position: int, shooter_proto: int, target_position: int, target_proto: int):
        return self._ffi.uwTestShooting(shooter_position, shooter_proto, target_position, target_proto)

    def distance_line(self, ai: int, bi: int) -> float:
        a: Vector3 = self._positions[ai]
        b: Vector3 = self._positions[bi]
        x: float = a.x - b.x
        y: float = a.y - b.y
        z: float = a.z - b.z
        x *= x
        y *= y
        z *= z
        return math.sqrt(x + y + z)

    def distance_estimate(self, a: int, b: int) -> float:
        return self._api.uwDistanceEstimate(a, b)

    def yaw(self, a: int, b: int) -> float:
        return self._api.uwDistanceEstimate(a, b)

    def test_construction_placement(self, construction_prototype: int, position: int) -> bool:
        return self._api.uwTestConstructionPlacement(construction_prototype, position)

    def find_construction_placement(self, construction_prototype: int, position: int) -> bool:
        return self._api.uwFindConstructionPlacement(construction_prototype, position)

    def _load(self):
        print("loading map")
        self._positions = []
        self._ups = []
        self._neighbors = []
        self._terrains = []
        self._overview = []

        info = self._ffi.new("struct UwMapInfo *")
        self._ffi.uwMapInfo(info)
        self._name = self._ffi.string(info.name)
        self._guid = self._ffi.string(info.guid)
        self._path = self._ffi.string(info.path)
        self._max_players = info.maxPlayers
        print(f"map name: {self._name}")
        print(f"map guid: {self._guid}")

        count = self._api.uwTilesCount()
        tile = self._ffi.new("struct UwTile *")
        for i in range(count):
            self._api.uwTile(i, tile)
            p = Vector3(tile.position[0], tile.position[1], tile.position[2])
            self._positions.append(p)
            u = Vector3(tile.up[0], tile.up[1], tile.up[2])
            self._ups.append(u)
            n = self._ffi.unpack(tile.neighborsIndices, tile.neighborsCount)
            if n:
                self._neighbors.append(n)
            self._terrains.append(tile.terrain)

        print("map loaded")

    def _map_state_changed(self, map_state: MapState):
        if map_state == MapState.Loaded:
            self._load()

    def _updating(self, stepping: bool):
        if stepping:
            ex = self._ffi.new("struct UwOverviewExtract *")
            self._api.uwOverviewExtract()
            if ex.count > 0:
                self._overview = [OverviewFlags(i) for i in self._ffi.unmarshal(ex.flags, ex.count)]
        else:
            self._overview = []
