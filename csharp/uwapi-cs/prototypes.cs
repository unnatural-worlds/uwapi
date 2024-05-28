using System;
using System.Runtime.InteropServices;
using System.Collections.Generic;
using System.Text.Json;

namespace Unnatural
{
    public class ProtoResource
    {
        public uint id;
        public string name;
    }

    public class ProtoRecipe
    {
        public uint id;
        public string name;
        public Dictionary<uint, uint> inputs;
        public Dictionary<uint, uint> outputs;
        public uint duration;
        public uint placeOver;
    }

    public class ProtoConstruction
    {
        public uint id;
        public string name;
        public Dictionary<uint, uint> inputs;
        public uint output;
    }

    public class ProtoUnit
    {
        public uint id;
        public string name;
        public List<uint> recipes;
        public bool logistics;
        public bool assembler;
        public bool vital;
        public uint maxLife;
        public uint armorType;

        // weapon
        public uint damageType;
        public float dps;
        public float fireRange;
        public float rateOfFire;

        // mobile only
        public Dictionary<uint, float> speeds;
        public bool cargo;

        // building only
        public float buildingRadius;
    }

    public class HitChancesTable
    {
        public List<string> armorNames;
        public List<string> damageNames;
        public List<List<float>> hitChancesTable;
    }

    public class TerrainTypesTable
    {
        public List<string> terrainNames;
    }

    internal class Definitions
    {
        public HitChancesTable hitChancesTable;
        public TerrainTypesTable terrainTypesTable;
    }

    internal class ProtoGeneric
    {
        public uint type;
        public string name;
        public string json;
    }

    public static class Prototypes
    {
        public static IReadOnlyList<uint> All()
        {
            return all;
        }

        public static uint Type(uint id)
        {
            ProtoGeneric tmp;
            return types.TryGetValue(id, out tmp) ? tmp.type : 0;
        }

        public static string Name(uint id)
        {
            ProtoGeneric tmp;
            return types.TryGetValue(id, out tmp) ? tmp.name : "";
        }

        public static string Json(uint id)
        {
            ProtoGeneric tmp;
            return types.TryGetValue(id, out tmp) ? tmp.json : "";
        }

        public static ProtoResource Resource(uint id)
        {
            ProtoResource tmp;
            return resources.TryGetValue(id, out tmp) ? tmp : null;
        }

        public static ProtoRecipe Recipe(uint id)
        {
            ProtoRecipe tmp;
            return recipes.TryGetValue(id, out tmp) ? tmp : null;
        }

        public static ProtoConstruction Construction(uint id)
        {
            ProtoConstruction tmp;
            return constructions.TryGetValue(id, out tmp) ? tmp : null;
        }

        public static ProtoUnit Unit(uint id)
        {
            ProtoUnit tmp;
            return units.TryGetValue(id, out tmp) ? tmp : null;
        }

        public static HitChancesTable HitChancesTable()
        {
            return hitChancesTable;
        }

        public static TerrainTypesTable TerrainTypesTable()
        {
            return terrainTypesTable;
        }

        static readonly List<uint> all = new List<uint>();
        static readonly Dictionary<uint, ProtoGeneric> types = new Dictionary<uint, ProtoGeneric>();
        static readonly Dictionary<uint, ProtoResource> resources = new Dictionary<uint, ProtoResource>();
        static readonly Dictionary<uint, ProtoRecipe> recipes = new Dictionary<uint, ProtoRecipe>();
        static readonly Dictionary<uint, ProtoConstruction> constructions = new Dictionary<uint, ProtoConstruction>();
        static readonly Dictionary<uint, ProtoUnit> units = new Dictionary<uint, ProtoUnit>();
        static HitChancesTable hitChancesTable;
        static TerrainTypesTable terrainTypesTable;

        static uint[] AllIds()
        {
            Interop.UwIds ids = new Interop.UwIds();
            Interop.uwAllPrototypes(ref ids);
            return InteropHelpers.Ids(ids);
        }

        static void LoadPrototypes()
        {
            Console.WriteLine("loading prototypes");

            all.Clear();
            types.Clear();
            resources.Clear();
            recipes.Clear();
            constructions.Clear();
            units.Clear();

            var options = new JsonSerializerOptions
            {
                IncludeFields = true,
            };

            foreach (uint id in AllIds())
            {
                ProtoGeneric pg = new ProtoGeneric();
                pg.type = Interop.uwPrototypeType(id);
                pg.json = Marshal.PtrToStringAnsi(Interop.uwPrototypeJson(id));
                switch (pg.type)
                {
                    case 1:
                        resources[id] = JsonSerializer.Deserialize<ProtoResource>(pg.json, options);
                        pg.name = resources[id].name;
                        break;
                    case 2:
                        recipes[id] = JsonSerializer.Deserialize<ProtoRecipe>(pg.json, options);
                        pg.name = recipes[id].name;
                        break;
                    case 3:
                        constructions[id] = JsonSerializer.Deserialize<ProtoConstruction>(pg.json, options);
                        pg.name = constructions[id].name;
                        break;
                    case 4:
                        units[id] = JsonSerializer.Deserialize<ProtoUnit>(pg.json, options);
                        pg.name = units[id].name;
                        break;
                }
                types[id] = pg;
                all.Add(id);
            }

            Console.WriteLine("prototypes loaded");
        }

        static void LoadDefinitions()
        {
            Console.WriteLine("loading definitions");

            var options = new JsonSerializerOptions
            {
                IncludeFields = true,
            };

            string json = Marshal.PtrToStringAnsi(Interop.uwDefinitionsJson());
            Definitions defs = JsonSerializer.Deserialize<Definitions>(json, options);
            hitChancesTable = defs.hitChancesTable;
            terrainTypesTable = defs.terrainTypesTable;

            Console.WriteLine("definitions loaded");
        }

        static void Preparing(object sender, EventArgs e)
        {
            LoadPrototypes();
            LoadDefinitions();
        }

        static Prototypes()
        {
            Game.Preparing += Preparing;
        }
    }
}
