using System.Runtime.InteropServices;

namespace Unnatural
{
    using Order = Interop.UwOrder;
    using Type = Interop.UwOrderTypeEnum;
    using Priority = Interop.UwOrderPriorityFlags;

    public static class Commands
    {
        const uint Invalid = 4294967295;

        public static Order[] Orders(uint unit)
        {
            Interop.UwOrders os = new Interop.UwOrders();
            Interop.uwOrders(unit, ref os);
            Order[] tmp = new Order[os.count];
            for (int i = 0; i < os.count; i++)
                tmp[i] = Marshal.PtrToStructure<Order>(os.orders + i * Marshal.SizeOf<Order>());
            return tmp;
        }

        public static void Order(uint unit, Order order)
        {
            Interop.uwOrder(unit, ref order);
        }

        public static Order Stop()
        {
            Order o = new Order();
            o.entity = Invalid;
            o.position = Invalid;
            o.order = Type.Stop;
            o.priority = Priority.User;
            return o;
        }

        public static Order Guard()
        {
            Order o = new Order();
            o.entity = Invalid;
            o.position = Invalid;
            o.order = Type.Guard;
            o.priority = Priority.User;
            return o;
        }

        public static Order RunToPosition(uint position)
        {
            Order o = new Order();
            o.entity = Invalid;
            o.position = position;
            o.order = Type.Run;
            o.priority = Priority.User;
            return o;
        }

        public static Order RunToEntity(uint entity)
        {
            Order o = new Order();
            o.entity = entity;
            o.position = Invalid;
            o.order = Type.Run;
            o.priority = Priority.User;
            return o;
        }

        public static Order FightToPosition(uint position)
        {
            Order o = new Order();
            o.entity = Invalid;
            o.position = position;
            o.order = Type.Fight;
            o.priority = Priority.User;
            return o;
        }

        public static Order FightToEntity(uint entity)
        {
            Order o = new Order();
            o.entity = entity;
            o.position = Invalid;
            o.order = Type.Fight;
            o.priority = Priority.User;
            return o;
        }

        public static void PlaceConstruction(uint constructionProto, uint position, float yaw = 0, uint recipeProto = 0, Interop.UwPriorityEnum priority = Interop.UwPriorityEnum.Normal)
        {
            Interop.uwCommandPlaceConstruction(constructionProto, position, yaw, recipeProto, priority);
        }

        public static void SetRecipe(uint unit, uint recipe)
        {
            Interop.uwCommandSetRecipe(unit, recipe);
        }

        public static void SetPriority(uint unit, Interop.UwPriorityEnum priority)
        {
            Interop.uwCommandSetPriority(unit, priority);
        }

        public static void Load(uint unit, uint resourceType)
        {
            Interop.uwCommandLoad(unit, resourceType);
        }

        public static void Unload(uint unit)
        {
            Interop.uwCommandUnload(unit);
        }

        public static void Move(uint unit, uint position, float yaw = 0)
        {
            Interop.uwCommandMove(unit, position, yaw);
        }

        public static void Aim(uint unit, uint target)
        {
            Interop.uwCommandAim(unit, target);
        }

        public static void RenounceControl(uint unit)
        {
            Interop.uwCommandRenounceControl(unit);
        }

        public static void SelfDestruct(uint unit)
        {
            Interop.uwCommandSelfDestruct(unit);
        }
    }
}
