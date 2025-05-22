using System;
using System.Runtime.InteropServices;

namespace Unnatural
{
    public static class InteropHelpers
    {
        public static uint[] Ids(Interop.UwIds ids)
        {
            uint[] tmp = new uint[ids.count];
            if (ids.count > 0)
                Marshal.Copy(ids.ids, (int[])(object)tmp, 0, (int)ids.count);
            return tmp;
        }
    }

    public static class UwapiTasks
    {
        public static ulong InsertTask(Action a)
        {
            ulong i = index++;
            actions.Add(i, a);
            return i;
        }

        static ulong index = 1;
        static System.Collections.Generic.Dictionary<ulong, Action> actions = new System.Collections.Generic.Dictionary<ulong, Action>();
        static readonly Interop.UwTaskCompletedCallbackType TaskCompletedDelegate = new Interop.UwTaskCompletedCallbackType(TaskCompleted);

        static void TaskCompleted(ulong taskUserData, Interop.UwTaskTypeEnum type)
        {
            if (type != Interop.UwTaskTypeEnum.None)
            {
                Action a;
                if (actions.TryGetValue(taskUserData, out a))
                    a();
            }
            actions.Remove(taskUserData);
        }

        static UwapiTasks()
        {
            Interop.uwSetTaskCompletedCallback(TaskCompletedDelegate);
        }

        public static void Init()
        { }
    }
}
