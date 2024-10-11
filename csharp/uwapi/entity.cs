using System;

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
    using Priority = Interop.UwPriorityComponent;
    using Amount = Interop.UwAmountComponent;
    using Attachment = Interop.UwAttachmentComponent;
    using Player = Interop.UwPlayerComponent;
    using Force = Interop.UwForceComponent;
    using ForceDetails = Interop.UwForceDetailsComponent;
    using ForeignPolicy = Interop.UwForeignPolicyComponent;
    using DiplomacyProposal = Interop.UwDiplomacyProposalComponent;
    using PolicyEnum = Interop.UwForeignPolicyEnum;

    public class Entity
    {
        public readonly uint id;
        public Proto? proto;
        public Owner? owner;
        public Controller? controller;
        public Position? position;
        public Unit? unit;
        public Life? life;
        public Move? move;
        public Aim? aim;
        public Recipe? recipe;
        public UpdateTimestamp? updateTimestamp;
        public RecipeStatistics? recipeStatistics;
        public Priority? priority;
        public Amount? amount;
        public Attachment? attachment;
        public Player? player;
        public Force? force;
        public ForceDetails? forceDetails;
        public ForeignPolicy? foreignPolicy;
        public DiplomacyProposal? diplomacyProposal;

        public Entity(uint id) { this.id = id; }

        public void FetchData()
        {
            IntPtr e = Interop.uwEntityPointer(id);
            {
                Proto tmp = new Proto();
                if (Interop.uwFetchProtoComponent(e, ref tmp))
                    proto = tmp;
                else
                    proto = null;
            }
            {
                Owner tmp = new Owner();
                if (Interop.uwFetchOwnerComponent(e, ref tmp))
                    owner = tmp;
                else
                    owner = null;
            }
            {
                Controller tmp = new Controller();
                if (Interop.uwFetchControllerComponent(e, ref tmp))
                    controller = tmp;
                else
                    controller = null;
            }
            {
                Position tmp = new Position();
                if (Interop.uwFetchPositionComponent(e, ref tmp))
                    position = tmp;
                else
                    position = null;
            }
            {
                Unit tmp = new Unit();
                if (Interop.uwFetchUnitComponent(e, ref tmp))
                    unit = tmp;
                else
                    unit = null;
            }
            {
                Life tmp = new Life();
                if (Interop.uwFetchLifeComponent(e, ref tmp))
                    life = tmp;
                else
                    life = null;
            }
            {
                Move tmp = new Move();
                if (Interop.uwFetchMoveComponent(e, ref tmp))
                    move = tmp;
                else
                    move = null;
            }
            {
                Aim tmp = new Aim();
                if (Interop.uwFetchAimComponent(e, ref tmp))
                    aim = tmp;
                else
                    aim = null;
            }
            {
                Recipe tmp = new Recipe();
                if (Interop.uwFetchRecipeComponent(e, ref tmp))
                    recipe = tmp;
                else
                    recipe = null;
            }
            {
                UpdateTimestamp tmp = new UpdateTimestamp();
                if (Interop.uwFetchUpdateTimestampComponent(e, ref tmp))
                    updateTimestamp = tmp;
                else
                    updateTimestamp = null;
            }
            {
                RecipeStatistics tmp = new RecipeStatistics();
                if (Interop.uwFetchRecipeStatisticsComponent(e, ref tmp))
                    recipeStatistics = tmp;
                else
                    recipeStatistics = null;
            }
            {
                Priority tmp = new Priority();
                if (Interop.uwFetchPriorityComponent(e, ref tmp))
                    priority = tmp;
                else
                    priority = null;
            }
            {
                Amount tmp = new Amount();
                if (Interop.uwFetchAmountComponent(e, ref tmp))
                    amount = tmp;
                else
                    amount = null;
            }
            {
                Attachment tmp = new Attachment();
                if (Interop.uwFetchAttachmentComponent(e, ref tmp))
                    attachment = tmp;
                else
                    attachment = null;
            }
            {
                Player tmp = new Player();
                if (Interop.uwFetchPlayerComponent(e, ref tmp))
                    player = tmp;
                else
                    player = null;
            }
            {
                Force tmp = new Force();
                if (Interop.uwFetchForceComponent(e, ref tmp))
                    force = tmp;
                else
                    force = null;
            }
            {
                ForceDetails tmp = new ForceDetails();
                if (Interop.uwFetchForceDetailsComponent(e, ref tmp))
                    forceDetails = tmp;
                else
                    forceDetails = null;
            }
            {
                ForeignPolicy tmp = new ForeignPolicy();
                if (Interop.uwFetchForeignPolicyComponent(e, ref tmp))
                    foreignPolicy = tmp;
                else
                    foreignPolicy = null;
            }
            {
                DiplomacyProposal tmp = new DiplomacyProposal();
                if (Interop.uwFetchDiplomacyProposalComponent(e, ref tmp))
                    diplomacyProposal = tmp;
                else
                    diplomacyProposal = null;
            }
        }

        public bool Own()
        {
            return owner.HasValue ? owner.Value.force == World.MyForce() : false;
        }

        public PolicyEnum Policy()
        {
            return owner.HasValue ? World.Policy(owner.Value.force) : PolicyEnum.None;
        }
    }
}
