using System.Runtime.InteropServices;
using System.Collections.Generic;
using System.Text.Json;

namespace Unnatural
{
    using MapStateEnum = Interop.UwMapStateEnum;
    using PrototypeTypeEnum = Interop.UwPrototypeTypeEnum;

    public class ProtoCommon
    {
        public uint id;
        public string name;
        public string json;
        public PrototypeTypeEnum type;
        public string[] tags;

        public bool Tagged(string tag)
        {
            foreach (var t in tags)
                if (t == tag)
                    return true;
            return false;
        }
    }

    public class ProtoResource : ProtoCommon
    {
        // nothing for now
    }

    public class ProtoRecipe : ProtoCommon
    {
        public Dictionary<uint, uint> inputs; // id -> count
        public Dictionary<uint, uint> outputs; // id -> count
        public uint duration; // ticks
        public uint placeOver; // id of unit
    }

    public class ProtoConstruction : ProtoCommon
    {
        public Dictionary<uint, uint> inputs; // id -> count
        public uint output; // id of unit
    }

    public class ProtoUnit : ProtoCommon
    {
        public List<uint> recipes;
        public bool logistics; // vehicle that is automatically controlled by the logistics system
        public bool assembler; // the unit must have at least one valid recipe
        public bool vital; // a force loses when it loses last vital unit
        public uint maxLife;
        public uint armorType;

        // weapon
        public uint damageType;
        public float dps;
        public float dpsAtLowLife;
        public float fireRange; // meters
        public float rateOfFire;

        // mobile only
        public Dictionary<uint, float> speeds; // terrain type -> speed (meters per second)
        public bool cargo; // the unit may carry resources

        // building only
        public float buildingRadius; // meters
    }

    public class HitChancesTable
    {
        public List<string> armorNames;
        public List<string> damageNames;
        public List<List<float>> hitChancesTable; // damage type -> armor type -> damage chance
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

    public static class Prototypes
    {
        public static IReadOnlyList<uint> All()
        {
            return all;
        }

        public static PrototypeTypeEnum Type(uint id)
        {
            ProtoCommon tmp;
            return commons.TryGetValue(id, out tmp) ? tmp.type : PrototypeTypeEnum.None;
        }

        public static string Name(uint id)
        {
            ProtoCommon tmp;
            return commons.TryGetValue(id, out tmp) ? tmp.name : "";
        }

        public static string Json(uint id)
        {
            ProtoCommon tmp;
            return commons.TryGetValue(id, out tmp) ? tmp.json : "";
        }

        public static ProtoCommon Common(uint id)
        {
            ProtoCommon tmp;
            if (commons.TryGetValue(id, out tmp))
                return tmp;
            return null;
        }

        public static ProtoResource Resource(uint id)
        {
            ProtoCommon tmp;
            if (commons.TryGetValue(id, out tmp))
                if (tmp.type == PrototypeTypeEnum.Resource)
                    return (ProtoResource)tmp;
            return null;
        }

        public static ProtoRecipe Recipe(uint id)
        {
            ProtoCommon tmp;
            if (commons.TryGetValue(id, out tmp))
                if (tmp.type == PrototypeTypeEnum.Recipe)
                    return (ProtoRecipe)tmp;
            return null;
        }

        public static ProtoConstruction Construction(uint id)
        {
            ProtoCommon tmp;
            if (commons.TryGetValue(id, out tmp))
                if (tmp.type == PrototypeTypeEnum.Construction)
                    return (ProtoConstruction)tmp;
            return null;
        }

        public static ProtoUnit Unit(uint id)
        {
            ProtoCommon tmp;
            if (commons.TryGetValue(id, out tmp))
                if (tmp.type == PrototypeTypeEnum.Unit)
                    return (ProtoUnit)tmp;
            return null;
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
        static readonly Dictionary<uint, ProtoCommon> commons = new Dictionary<uint, ProtoCommon>();
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
            Game.LogInfo("loading prototypes");

            all.Clear();
            commons.Clear();

            var options = new JsonSerializerOptions
            {
                IncludeFields = true,
            };

            foreach (uint id in AllIds())
            {
                PrototypeTypeEnum type = Interop.uwPrototypeType(id);
                string json = Marshal.PtrToStringAnsi(Interop.uwPrototypeJson(id));
                ProtoCommon pc;
                switch (type)
                {
                    case PrototypeTypeEnum.Resource:
                        pc = JsonSerializer.Deserialize<ProtoResource>(json, options);
                        break;
                    case PrototypeTypeEnum.Recipe:
                        pc = JsonSerializer.Deserialize<ProtoRecipe>(json, options);
                        break;
                    case PrototypeTypeEnum.Construction:
                        pc = JsonSerializer.Deserialize<ProtoConstruction>(json, options);
                        break;
                    case PrototypeTypeEnum.Unit:
                        pc = JsonSerializer.Deserialize<ProtoUnit>(json, options);
                        break;
                    default:
                        throw new System.Exception("unknown prototype type enum");
                }
                pc.json = json;
                commons[id] = pc;
                all.Add(id);
            }

            Game.LogInfo("prototypes loaded");
        }

        static void LoadDefinitions()
        {
            Game.LogInfo("loading definitions");

            var options = new JsonSerializerOptions
            {
                IncludeFields = true,
            };

            string json = Marshal.PtrToStringAnsi(Interop.uwDefinitionsJson());
            Definitions defs = JsonSerializer.Deserialize<Definitions>(json, options);
            hitChancesTable = defs.hitChancesTable;
            terrainTypesTable = defs.terrainTypesTable;

            Game.LogInfo("definitions loaded");
        }

        static void MapStateChanged(object sender, MapStateEnum state)
        {
            if (state == MapStateEnum.Loaded)
            {
                LoadPrototypes();
                LoadDefinitions();
            }
        }

        static Prototypes()
        {
            Game.MapStateChanged += MapStateChanged;
        }
    }
}
