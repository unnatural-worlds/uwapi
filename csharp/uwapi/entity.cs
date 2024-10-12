namespace Unnatural
{
    using PolicyEnum = Interop.UwForeignPolicyEnum;
    using TypeEnum = Interop.UwPrototypeTypeEnum;

    public partial class Entity
    {
        const uint Invalid = 4294967295;

        public readonly uint Id;

        public Entity(uint id) { Id = id; }

        public bool Own()
        {
            return Owner.HasValue && Owner.Value.force == World.MyForceId();
        }

        public bool Ally()
        {
            return Owner.HasValue && World.Policy(Owner.Value.force) == PolicyEnum.Ally;
        }

        public bool Enemy()
        {
            return Owner.HasValue && World.Policy(Owner.Value.force) == PolicyEnum.Enemy;
        }

        public PolicyEnum Policy()
        {
            return Owner.HasValue ? World.Policy(Owner.Value.force) : PolicyEnum.None;
        }

        public TypeEnum Type()
        {
            return Proto.HasValue ? Prototypes.Type(Proto.Value.proto) : TypeEnum.None;
        }

        public uint Pos()
        {
            return Position.HasValue ? Position.Value.position : Invalid;
        }
    }
}
