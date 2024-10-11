namespace Unnatural
{
    using PolicyEnum = Interop.UwForeignPolicyEnum;

    public partial class Entity
    {
        public readonly uint Id;

        public Entity(uint id) { Id = id; }

        public bool Own()
        {
            return Owner.HasValue && Owner.Value.force == World.MyForce();
        }

        public PolicyEnum Policy()
        {
            return Owner.HasValue ? World.Policy(Owner.Value.force) : PolicyEnum.None;
        }
    }
}
