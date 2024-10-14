namespace Unnatural
{
    using PolicyEnum = Interop.UwForeignPolicyEnum;
    using TypeEnum = Interop.UwPrototypeTypeEnum;

    public partial class Entity
    {
        const uint Invalid = 4294967295;

        public readonly uint Id;

        public Entity(uint id) { Id = id; }

        public uint Pos => Position.HasValue ? Position.Value.position : Invalid;

        public PolicyEnum Policy => Owner.HasValue ? World.Policy(Owner.Value.force) : PolicyEnum.None;

        public bool Own => Owner.HasValue && Owner.Value.force == World.MyForceId();

        public bool Ally => Owner.HasValue && World.Policy(Owner.Value.force) == PolicyEnum.Ally;

        public bool Enemy => Owner.HasValue && World.Policy(Owner.Value.force) == PolicyEnum.Enemy;

        public TypeEnum Type => Proto.HasValue ? Prototypes.Type(Proto.Value.proto) : TypeEnum.None;

        public ProtoCommon ProtoCommon => Proto.HasValue ? Prototypes.Common(Proto.Value.proto) : null;

        public ProtoResource ProtoResource => Proto.HasValue ? Prototypes.Resource(Proto.Value.proto) : null;

        // an entity cannot be a recipe on its own

        public ProtoConstruction ProtoConstruction => Proto.HasValue ? Prototypes.Construction(Proto.Value.proto) : null;

        public ProtoUnit ProtoUnit => Proto.HasValue ? Prototypes.Unit(Proto.Value.proto) : null;

        public bool Tagged(string tag)
        {
            ProtoCommon p = ProtoCommon;
            if (p != null)
                return p.Tagged(tag);
            return false;
        }
    }
}
