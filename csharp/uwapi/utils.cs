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
}
