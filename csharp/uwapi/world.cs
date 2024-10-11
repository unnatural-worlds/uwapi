using System.Collections.Generic;

namespace Unnatural
{
    using ForeignPolicy = Interop.UwForeignPolicyComponent;
    using PolicyEnum = Interop.UwForeignPolicyEnum;

    public static class World
    {
        public static uint MyForce()
        {
            return myForce;
        }

        public static IReadOnlyDictionary<uint, Entity> Entities()
        {
            return entities;
        }

        public static Entity Entity(uint id)
        {
            return entities[id];
        }

        public static PolicyEnum Policy(uint force)
        {
            PolicyEnum val;
            return policies.TryGetValue(force, out val) ? val : PolicyEnum.None;
        }

        static uint myForce;
        static readonly Dictionary<uint, Entity> entities = new Dictionary<uint, Entity>();
        static readonly Dictionary<uint, PolicyEnum> policies = new Dictionary<uint, PolicyEnum>();

        static uint[] AllIds()
        {
            Interop.UwIds ids = new Interop.UwIds();
            Interop.uwAllEntities(ref ids);
            return InteropHelpers.Ids(ids);
        }

        static uint[] ModifiedIds()
        {
            Interop.UwIds ids = new Interop.UwIds();
            Interop.uwModifiedEntities(ref ids);
            return InteropHelpers.Ids(ids);
        }

        static void UpdateRemoved()
        {
            var allIds = new HashSet<uint>(AllIds());
            var removed = new List<uint>();
            foreach (uint id in entities.Keys)
                if (!allIds.Contains(id))
                    removed.Add(id);
            foreach (uint id in removed)
                entities.Remove(id);
        }

        static void UpdateModified()
        {
            foreach (uint id in ModifiedIds())
            {
                if (entities.ContainsKey(id))
                {
                    entities[id].FetchComponents();
                }
                else
                {
                    Entity o = new Entity(id);
                    o.FetchComponents();
                    entities[id] = o;
                }
            }
        }

        static void UpdatePolicies()
        {
            policies.Clear();
            foreach (Entity e in entities.Values)
            {
                if (!e.ForeignPolicy.HasValue)
                    continue;
                ForeignPolicy fp = e.ForeignPolicy.Value;
                if (fp.forces[0] == myForce)
                    policies[fp.forces[1]] = fp.policy;
                if (fp.forces[1] == myForce)
                    policies[fp.forces[0]] = fp.policy;
            }
        }

        static void Updating(object sender, bool stepping)
        {
            {
                Interop.UwMyPlayer tmp = new Interop.UwMyPlayer();
                Interop.uwMyPlayer(ref tmp);
                myForce = tmp.forceEntityId;
            }
            UpdateRemoved();
            UpdateModified();
            UpdatePolicies();
        }

        static World()
        {
            Game.Updating += Updating;
        }
    }
}
