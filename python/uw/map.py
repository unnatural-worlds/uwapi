from .helpers import MapState
from .helpers import OverviewFlags
from .game import Game


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class Map:
    def __init__(self, api, ffi, game: Game):
        self._api = api
        self._ffi = ffi
        self._game = game

        # TODO
        self._game.add_map_state_callback(self._map_state_changed)
        self._game.add_update_callback(self._updating)

        self._name: str = ""
        self._guid: str = ""
        self._path: str = ""
        self._map_players: int = 0
        self._positions: list[Vector3] = []
        self._ups: list[Vector3] = []
        self._neighbors: list[list[int]] = []
        self._terrains: list[bytes] = []
        self._overview: list[OverviewFlags] = []

    def name(self) -> str:
        return self._name

    def guid(self) -> str:
        return self._guid

    #         public static string Path()
    #         {
    #             return path;
    #         }
    #
    #         public static uint MaxPlayers()
    #         {
    #             return maxPlayers;
    #         }
    #
    #         public static IReadOnlyList<Vector3> Positions()
    #         {
    #             return positions;
    #         }
    #
    #         public static IReadOnlyList<Vector3> Ups()
    #         {
    #             return ups;
    #         }
    #
    #         public static IReadOnlyList<IReadOnlyList<uint>> Neighbors()
    #         {
    #             return neighbors;
    #         }
    #
    #         public static IReadOnlyList<uint> Neighbors(uint position)
    #         {
    #             return neighbors[(int)position];
    #         }
    #
    #         public static IReadOnlyList<byte> Terrains()
    #         {
    #             return terrains;
    #         }
    #
    #         public static IReadOnlyList<OverviewFlags> Overview()
    #         {
    #             return overview;
    #         }
    #
    #         public static uint[] Entities(uint position)
    #         {
    #             Interop.UwIds ns = new Interop.UwIds();
    #             Interop.uwOverviewIds(position, ref ns);
    #             return InteropHelpers.Ids(ns);
    #         }
    #
    #         public static uint[] AreaRange(Vector3 point, float radius)
    #         {
    #             Interop.UwIds tiles = new Interop.UwIds();
    #             Interop.uwAreaRange(point.x, point.y, point.z, radius, ref tiles);
    #             return InteropHelpers.Ids(tiles);
    #         }
    #
    #         public static uint[] AreaConnected(uint position, float radius)
    #         {
    #             Interop.UwIds tiles = new Interop.UwIds();
    #             Interop.uwAreaConnected(position, radius, ref tiles);
    #             return InteropHelpers.Ids(tiles);
    #         }
    #
    #         public static uint[] AreaNeighborhood(uint position, float radius)
    #         {
    #             Interop.UwIds tiles = new Interop.UwIds();
    #             Interop.uwAreaNeighborhood(position, radius, ref tiles);
    #             return InteropHelpers.Ids(tiles);
    #         }
    #
    #         public static uint[] AreaExtended(uint position, float radius)
    #         {
    #             Interop.UwIds tiles = new Interop.UwIds();
    #             Interop.uwAreaExtended(position, radius, ref tiles);
    #             return InteropHelpers.Ids(tiles);
    #         }
    #
    #         public static bool TestVisible(Vector3 a, Vector3 b)
    #         {
    #             return Interop.uwTestVisible(a.x, a.y, a.z, b.x, b.y, b.z);
    #         }
    #
    #         public static bool TestShooting(uint shooterPosition, uint shooterProto, uint targetPosition, uint targetProto)
    #         {
    #             return Interop.uwTestShooting(shooterPosition, shooterProto, targetPosition, targetProto);
    #         }
    #
    #         public static float DistanceLine(uint ai, uint bi)
    #         {
    #             Vector3 a = positions[(int)ai];
    #             Vector3 b = positions[(int)bi];
    #             float x = a.x - b.x;
    #             float y = a.y - b.y;
    #             float z = a.z - b.z;
    #             x *= x;
    #             y *= y;
    #             z *= z;
    #             return (float)Math.Sqrt(x + y + z);
    #         }
    #
    #         public static float DistanceEstimate(uint a, uint b)
    #         {
    #             return Interop.uwDistanceEstimate(a, b);
    #         }
    #
    #         public static float Yaw(uint a, uint b)
    #         {
    #             return Interop.uwYaw(a, b);
    #         }
    #
    #         public static bool TestConstructionPlacement(uint constructionPrototype, uint position)
    #         {
    #             return Interop.uwTestConstructionPlacement(constructionPrototype, position);
    #         }
    #
    #         public static uint FindConstructionPlacement(uint constructionPrototype, uint position)
    #         {
    #             return Interop.uwFindConstructionPlacement(constructionPrototype, position);
    #         }
    #
    #
    #
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
        self._map_players = info.maxPlayers
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

#     }
#
#     public static class InteropHelpers
#     {
#         public static uint[] Ids(Interop.UwIds ids)
#         {
#             uint[] tmp = new uint[ids.count];
#             if (ids.count > 0)
#                 Marshal.Copy(ids.ids, (int[])(object)tmp, 0, (int)ids.count);
#             return tmp;
#         }
#     }
