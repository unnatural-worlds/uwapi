using System;
using System.Collections.Generic;
using System.Dynamic;

namespace Unnatural
{
    using Proto = Interop.UwProtoComponent;
    using Owner = Interop.UwOwnerComponent;
    using Controller = Interop.UwControllerComponent;
    using Position = Interop.UwPositionComponent;
    using Unit = Interop.UwUnitComponent;
    using Life = Interop.UwLifeComponent;
    using Move = Interop.UwMoveComponent;
    using Aim = Interop.UwAimComponent;
    using Recipe = Interop.UwRecipeComponent;
    using UpdateTimestamp = Interop.UwUpdateTimestampComponent;
    using RecipeStatistics = Interop.UwRecipeStatisticsComponent;
    using Amount = Interop.UwAmountComponent;
    using Attachment = Interop.UwAttachmentComponent;
    using Player = Interop.UwPlayerComponent;
    using Force = Interop.UwForceComponent;
    using ForceDetails = Interop.UwForceDetailsComponent;
    using ForeignPolicy = Interop.UwForeignPolicyComponent;
    using DiplomacyProposal = Interop.UwDiplomacyProposalComponent;
    using PolicyEnum = Interop.UwForeignPolicyEnum;

    public static class Entity
    {
        public static bool Has(dynamic entity, string component)
        {
            return ((IDictionary<string, object>)entity).ContainsKey(component);
        }

        public static bool Has(dynamic entity, IEnumerable<string> components)
        {
            foreach (var c in components)
                if (!Has(entity, c))
                    return false;
            return true;
        }

        public static bool Own(dynamic entity)
        {
            return Has(entity, "Owner") && entity.Owner.force == World.MyForce();
        }

        public static PolicyEnum Policy(dynamic entity)
        {
            if (!Has(entity, "Owner"))
                return PolicyEnum.None;
            return World.Policy(entity.Owner.force);
        }
    }

    public static class World
    {
        public static uint MyForce()
        {
            return myForce;
        }

        public static IReadOnlyDictionary<uint, dynamic> Entities()
        {
            return entities;
        }

        public static dynamic Entity(uint id)
        {
            return entities[id];
        }

        public static PolicyEnum Policy(uint force)
        {
            PolicyEnum val;
            return policies.TryGetValue(force, out val) ? val : PolicyEnum.None;
        }

        static uint myForce;
        static readonly Dictionary<uint, dynamic> entities = new Dictionary<uint, dynamic>();
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
                dynamic o = entities.ContainsKey(id) ? entities[id] : new ExpandoObject();
                o.Id = id;
                entities[id] = o;
                IntPtr e = Interop.uwEntityPointer(id);
                {
                    Proto tmp = new Proto();
                    if (Interop.uwFetchProtoComponent(e, ref tmp))
                        o.Proto = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Proto");
                }
                {
                    Owner tmp = new Owner();
                    if (Interop.uwFetchOwnerComponent(e, ref tmp))
                        o.Owner = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Owner");
                }
                {
                    Controller tmp = new Controller();
                    if (Interop.uwFetchControllerComponent(e, ref tmp))
                        o.Controller = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Controller");
                }
                {
                    Position tmp = new Position();
                    if (Interop.uwFetchPositionComponent(e, ref tmp))
                        o.Position = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Position");
                }
                {
                    Unit tmp = new Unit();
                    if (Interop.uwFetchUnitComponent(e, ref tmp))
                        o.Unit = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Unit");
                }
                {
                    Life tmp = new Life();
                    if (Interop.uwFetchLifeComponent(e, ref tmp))
                        o.Life = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Life");
                }
                {
                    Move tmp = new Move();
                    if (Interop.uwFetchMoveComponent(e, ref tmp))
                        o.Move = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Move");
                }
                {
                    Aim tmp = new Aim();
                    if (Interop.uwFetchAimComponent(e, ref tmp))
                        o.Aim = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Aim");
                }
                {
                    Recipe tmp = new Recipe();
                    if (Interop.uwFetchRecipeComponent(e, ref tmp))
                        o.Recipe = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Recipe");
                }
                {
                    UpdateTimestamp tmp = new UpdateTimestamp();
                    if (Interop.uwFetchUpdateTimestampComponent(e, ref tmp))
                        o.UpdateTimestamp = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("UpdateTimestamp");
                }
                {
                    RecipeStatistics tmp = new RecipeStatistics();
                    if (Interop.uwFetchRecipeStatisticsComponent(e, ref tmp))
                        o.RecipeStatistics = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("RecipeStatistics");
                }
                {
                    Amount tmp = new Amount();
                    if (Interop.uwFetchAmountComponent(e, ref tmp))
                        o.Amount = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Amount");
                }
                {
                    Attachment tmp = new Attachment();
                    if (Interop.uwFetchAttachmentComponent(e, ref tmp))
                        o.Attachment = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Attachment");
                }
                {
                    Player tmp = new Player();
                    if (Interop.uwFetchPlayerComponent(e, ref tmp))
                        o.Player = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Player");
                }
                {
                    Force tmp = new Force();
                    if (Interop.uwFetchForceComponent(e, ref tmp))
                        o.Force = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("Force");
                }
                {
                    ForceDetails tmp = new ForceDetails();
                    if (Interop.uwFetchForceDetailsComponent(e, ref tmp))
                        o.ForceDetails = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("ForceDetails");
                }
                {
                    ForeignPolicy tmp = new ForeignPolicy();
                    if (Interop.uwFetchForeignPolicyComponent(e, ref tmp))
                        o.ForeignPolicy = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("ForeignPolicy");
                }
                {
                    DiplomacyProposal tmp = new DiplomacyProposal();
                    if (Interop.uwFetchDiplomacyProposalComponent(e, ref tmp))
                        o.DiplomacyProposal = tmp;
                    else
                        ((IDictionary<string, object>)o).Remove("DiplomacyProposal");
                }
            }
        }

        static void UpdatePolicies()
        {
            policies.Clear();
            foreach (dynamic e in entities.Values)
            {
                if (!Unnatural.Entity.Has(e, "ForeignPolicy"))
                    continue;
                ForeignPolicy fp = e.ForeignPolicy;
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
