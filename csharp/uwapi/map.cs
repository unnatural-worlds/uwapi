using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;

namespace Unnatural
{
    using MapStateEnum = Interop.UwMapStateEnum;
    using OverviewFlags = Interop.UwOverviewFlags;

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

        public static Vector3 Position(uint position)
        {
            return positions[(int)position];
        }

        public static IReadOnlyList<Vector3> Ups()
        {
            return ups;
        }

        public static Vector3 Up(uint position)
        {
            return ups[(int)position];
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

        public static byte Terrain(uint position)
        {
            return terrains[(int)position];
        }

        public static IReadOnlyList<OverviewFlags> Overview()
        {
            return overview;
        }

        public static OverviewFlags Overview(uint position)
        {
            return overview[(int)position];
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

        public static bool TestShooting(uint shooterPosition, uint shooterProto, float shootingRangeUpgrade, uint targetPosition, uint targetProto)
        {
            return Interop.uwTestShooting(shooterPosition, shooterProto, shootingRangeUpgrade, targetPosition, targetProto);
        }

        public static bool TestShooting(uint shooterId, uint targetId)
        {
            return Interop.uwTestShootingEntities(shooterId, targetId);
        }

        public static float DistanceLine(uint a, uint b)
        {
            Vector3 a3 = positions[(int)a];
            Vector3 b3 = positions[(int)b];
            float x = a3.x - b3.x;
            float y = a3.y - b3.y;
            float z = a3.z - b3.z;
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

        public static IReadOnlyList<uint> TileToCluster()
        {
            return mapTileToCluster;
        }

        public static IReadOnlyList<uint> ClusterToTile()
        {
            return mapClusterToTile;
        }

        public static uint TileToCluster(uint tile)
        {
            return mapTileToCluster[(int)tile];
        }

        public static uint ClusterToTile(uint cluster)
        {
            return mapClusterToTile[(int)cluster];
        }

        public static IReadOnlyList<IReadOnlyList<uint>> ClustersNeighbors()
        {
            return clustersNeighbors;
        }

        public static IReadOnlyList<uint> ClustersNeighbors(uint cluster)
        {
            return clustersNeighbors[(int)cluster];
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
        static readonly List<uint> mapTileToCluster = new List<uint>();
        static readonly List<uint> mapClusterToTile = new List<uint>();
        static readonly List<uint[]> clustersNeighbors = new List<uint[]>();

        static void Load()
        {
            Game.LogInfo("loading map");

            positions.Clear();
            ups.Clear();
            neighbors.Clear();
            terrains.Clear();
            overview = new OverviewFlags[0];
            mapTileToCluster.Clear();
            mapClusterToTile.Clear();
            clustersNeighbors.Clear();

            {
                Interop.UwMapInfo info = new Interop.UwMapInfo();
                Interop.uwMapInfo(ref info);
                name = Marshal.PtrToStringAnsi(info.name);
                guid = Marshal.PtrToStringAnsi(info.guid);
                path = Marshal.PtrToStringAnsi(info.path);
                maxPlayers = info.maxPlayers;
            }

            {
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
                    mapTileToCluster.Add(tile.clusterIndex);
                }
            }

            {
                uint count = Interop.uwClustersCount();
                Interop.UwCluster cluster = new Interop.UwCluster();
                for (uint i = 0; i < count; ++i)
                {
                    Interop.uwCluster(i, ref cluster);
                    {
                        uint[] tmp = new uint[cluster.neighborsCount];
                        if (cluster.neighborsCount > 0)
                            Marshal.Copy(cluster.neighborsIndices, (int[])(object)tmp, 0, (int)cluster.neighborsCount);
                        clustersNeighbors.Add(tmp);
                    }
                    mapClusterToTile.Add(cluster.centerTileIndex);
                }
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
}
