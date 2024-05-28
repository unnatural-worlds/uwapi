using System.Runtime.InteropServices;

namespace Unnatural
{
    using Order = Interop.UwOrder;

    public static class Commands
    {
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
            o.entity = 4294967295;
            o.position = 4294967295;
            o.order = 1;
            o.priority = 2;
            return o;
        }

        public static Order Guard()
        {
            Order o = new Order();
            o.entity = 4294967295;
            o.position = 4294967295;
            o.order = 2;
            o.priority = 2;
            return o;
        }

        public static Order RunToPosition(uint position)
        {
            Order o = new Order();
            o.entity = 4294967295;
            o.position = position;
            o.order = 3;
            o.priority = 2;
            return o;
        }

        public static Order RunToEntity(uint entity)
        {
            Order o = new Order();
            o.entity = entity;
            o.position = 4294967295;
            o.order = 3;
            o.priority = 2;
            return o;
        }

        public static Order FightToPosition(uint position)
        {
            Order o = new Order();
            o.entity = 4294967295;
            o.position = position;
            o.order = 4;
            o.priority = 2;
            return o;
        }

        public static Order FightToEntity(uint entity)
        {
            Order o = new Order();
            o.entity = entity;
            o.position = 4294967295;
            o.order = 4;
            o.priority = 2;
            return o;
        }

        public static void CommandSelfDestruct(uint unit)
        {
            Interop.uwCommandSelfDestruct(unit);
        }

        public static void CommandPlaceConstruction(uint proto, uint position, float yaw = 0)
        {
            Interop.uwCommandPlaceConstruction(proto, position, yaw);
        }

        public static void CommandSetRecipe(uint unit, uint recipe)
        {
            Interop.uwCommandSetRecipe(unit, recipe);
        }

        public static void CommandLoad(uint unit, uint resourceType)
        {
            Interop.uwCommandLoad(unit, resourceType);
        }

        public static void CommandUnload(uint unit)
        {
            Interop.uwCommandUnload(unit);
        }

        public static void CommandMove(uint unit, uint position, float yaw = 0)
        {
            Interop.uwCommandMove(unit, position, yaw);
        }

        public static void CommandAim(uint unit, uint target)
        {
            Interop.uwCommandAim(unit, target);
        }

        public static void CommandRenounceControl(uint unit)
        {
            Interop.uwCommandRenounceControl(unit);
        }
    }
}
