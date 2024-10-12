using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;

namespace Unnatural
{
    using MapStateEnum = Interop.UwMapStateEnum;
    using OverviewFlags = Interop.UwOverviewFlags;
    using MapClusterStatistics = Interop.UwMapClusterStatistics;

    public struct Vector3
    {
        public float x, y, z;
    }

    public static class Map
    {
        public static string Name()
        {
            return name;
        }

        public static string Guid()
        {
            return guid;
        }

        public static string Path()
        {
            return path;
        }

        public static uint MaxPlayers()
        {
            return maxPlayers;
        }

        public static IReadOnlyList<Vector3> Positions()
        {
            return positions;
        }

        public static IReadOnlyList<Vector3> Ups()
        {
            return ups;
        }

        public static IReadOnlyList<IReadOnlyList<uint>> Neighbors()
        {
            return neighbors;
        }

        public static IReadOnlyList<uint> Neighbors(uint position)
        {
            return neighbors[(int)position];
        }

        public static IReadOnlyList<byte> Terrains()
        {
            return terrains;
        }

        public static IReadOnlyList<OverviewFlags> Overview()
        {
            return overview;
        }

        public static uint[] Entities(uint position)
        {
            Interop.UwIds ns = new Interop.UwIds();
            Interop.uwOverviewIds(position, ref ns);
            return InteropHelpers.Ids(ns);
        }

        public static uint[] AreaRange(Vector3 point, float radius)
        {
            Interop.UwIds tiles = new Interop.UwIds();
            Interop.uwAreaRange(point.x, point.y, point.z, radius, ref tiles);
            return InteropHelpers.Ids(tiles);
        }

        public static uint[] AreaConnected(uint position, float radius)
        {
            Interop.UwIds tiles = new Interop.UwIds();
            Interop.uwAreaConnected(position, radius, ref tiles);
            return InteropHelpers.Ids(tiles);
        }

        public static uint[] AreaNeighborhood(uint position, float radius)
        {
            Interop.UwIds tiles = new Interop.UwIds();
            Interop.uwAreaNeighborhood(position, radius, ref tiles);
            return InteropHelpers.Ids(tiles);
        }

        public static uint[] AreaExtended(uint position, float radius)
        {
            Interop.UwIds tiles = new Interop.UwIds();
            Interop.uwAreaExtended(position, radius, ref tiles);
            return InteropHelpers.Ids(tiles);
        }

        public static bool TestVisible(Vector3 a, Vector3 b)
        {
            return Interop.uwTestVisible(a.x, a.y, a.z, b.x, b.y, b.z);
        }

        public static bool TestShooting(uint shooterPosition, uint shooterProto, uint targetPosition, uint targetProto)
        {
            return Interop.uwTestShooting(shooterPosition, shooterProto, targetPosition, targetProto);
        }

        public static float DistanceLine(uint ai, uint bi)
        {
            Vector3 a = positions[(int)ai];
            Vector3 b = positions[(int)bi];
            float x = a.x - b.x;
            float y = a.y - b.y;
            float z = a.z - b.z;
            x *= x;
            y *= y;
            z *= z;
            return (float)Math.Sqrt(x + y + z);
        }

        public static float DistanceEstimate(uint a, uint b)
        {
            return Interop.uwDistanceEstimate(a, b);
        }

        public static float Yaw(uint a, uint b)
        {
            return Interop.uwYaw(a, b);
        }

        public static bool TestConstructionPlacement(uint constructionProto, uint position, uint recipeProto = 0)
        {
            return Interop.uwTestConstructionPlacement(constructionProto, position, recipeProto);
        }

        public static uint FindConstructionPlacement(uint constructionProto, uint position, uint recipeProto = 0)
        {
            return Interop.uwFindConstructionPlacement(constructionProto, position, recipeProto);
        }

        public static uint ClusterIndex(uint position)
        {
            return clusterIndices[(int)position];
        }

        public static IReadOnlyList<uint> ClusterIndices()
        {
            return clusterIndices;
        }

        public static IReadOnlyList<MapClusterStatistics> ClustersStatistics()
        {
            Interop.UwMapClustersStatisticsExtract ex = new Interop.UwMapClustersStatisticsExtract();
            Interop.uwMapClustersStatistics(ref ex);
            MapClusterStatistics[] tmp = new MapClusterStatistics[ex.count];
            for (int i = 0; i < ex.count; i++)
                tmp[i] = Marshal.PtrToStructure<MapClusterStatistics>(ex.stats + i * Marshal.SizeOf<MapClusterStatistics>());
            return tmp;
        }

        static string name;
        static string guid;
        static string path;
        static uint maxPlayers;
        static readonly List<Vector3> positions = new List<Vector3>();
        static readonly List<Vector3> ups = new List<Vector3>();
        static readonly List<uint[]> neighbors = new List<uint[]>();
        static readonly List<byte> terrains = new List<byte>();
        static OverviewFlags[] overview = new OverviewFlags[0];
        static readonly List<uint> clusterIndices = new List<uint>(); // maps tile index to cluster index

        static void Load()
        {
            Game.LogInfo("loading map");

            positions.Clear();
            ups.Clear();
            neighbors.Clear();
            terrains.Clear();
            overview = new OverviewFlags[0];
            clusterIndices.Clear();

            {
                Interop.UwMapInfo info = new Interop.UwMapInfo();
                Interop.uwMapInfo(ref info);
                name = Marshal.PtrToStringAnsi(info.name);
                guid = Marshal.PtrToStringAnsi(info.guid);
                path = Marshal.PtrToStringAnsi(info.path);
                maxPlayers = info.maxPlayers;
            }

            uint count = Interop.uwTilesCount();
            Interop.UwTile tile = new Interop.UwTile();
            for (uint i = 0; i < count; ++i)
            {
                Interop.uwTile(i, ref tile);
                {
                    Vector3 p = new Vector3();
                    p.x = tile.position[0];
                    p.y = tile.position[1];
                    p.z = tile.position[2];
                    positions.Add(p);
                }
                {
                    Vector3 u = new Vector3();
                    u.x = tile.up[0];
                    u.y = tile.up[1];
                    u.z = tile.up[2];
                    ups.Add(u);
                }
                {
                    uint[] tmp = new uint[tile.neighborsCount];
                    if (tile.neighborsCount > 0)
                        Marshal.Copy(tile.neighborsIndices, (int[])(object)tmp, 0, (int)tile.neighborsCount);
                    neighbors.Add(tmp);
                }
                terrains.Add(tile.terrain);
                clusterIndices.Add(tile.clusterIndex);
            }

            Game.LogInfo("map loaded");
        }

        static void MapStateChanged(object sender, MapStateEnum state)
        {
            if (state == MapStateEnum.Loaded)
                Load();
        }

        static void Updating(object sender, bool stepping)
        {
            if (stepping)
            {
                Interop.UwOverviewExtract ex = new Interop.UwOverviewExtract();
                Interop.uwOverviewExtract(ref ex);
                if (overview.Length != ex.count)
                    overview = new OverviewFlags[ex.count];
                if (ex.count > 0)
                    Marshal.Copy(ex.flags, (int[])(object)overview, 0, (int)ex.count);
            }
            else
                overview = new OverviewFlags[0];
        }

        static Map()
        {
            Game.MapStateChanged += MapStateChanged;
            Game.Updating += Updating;
        }
    }

    public static class InteropHelpers
    {
        public static uint[] Ids(Interop.UwIds ids)
        {
            uint[] tmp = new uint[ids.count];
            if (ids.count > 0)
                Marshal.Copy(ids.ids, (int[])(object)tmp, 0, (int)ids.count);
            return tmp;
        }
    }
}
