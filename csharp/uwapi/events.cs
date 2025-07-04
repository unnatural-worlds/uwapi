using System;
using System.Runtime.InteropServices;

namespace Unnatural
{
    using ConnectionStateEnum = Interop.UwConnectionStateEnum;
    using GameStateEnum = Interop.UwGameStateEnum;
    using MapStateEnum = Interop.UwMapStateEnum;
    using ShootingData = Interop.UwShootingData;
    using ShootingArray = Interop.UwShootingArray;
    using ExplosionData = Interop.UwExplosionData;
    using ExplosionsArray = Interop.UwExplosionsArray;
    using ChatTargetFLags = Interop.UwChatTargetFlags;

    public class ChatMessage
    {
        public string Message;
        public uint Sender;
        public ChatTargetFLags Flags;
    }

    public static class Events
    {

        public static event EventHandler<ConnectionStateEnum> ConnectionStateChanged;
        public static event EventHandler<GameStateEnum> GameStateChanged;
        public static event EventHandler<MapStateEnum> MapStateChanged;
        public static event EventHandler<bool> Updating;
        public static event EventHandler<ShootingData[]> Shooting;
        public static event EventHandler<ExplosionData[]> Explosions;
        public static event EventHandler<uint> ForceEliminated;
        public static event EventHandler<ChatMessage> ChatReceived;

        static readonly Interop.UwExceptionCallbackType ExceptionDelegate = new Interop.UwExceptionCallbackType(ExceptionCallback);
        static readonly Interop.UwConnectionStateCallbackType ConnectionStateDelegate = new Interop.UwConnectionStateCallbackType(ConnectionStateCallback);
        static readonly Interop.UwGameStateCallbackType GameStateDelegate = new Interop.UwGameStateCallbackType(GameStateCallback);
        static readonly Interop.UwMapStateCallbackType MapStateDelegate = new Interop.UwMapStateCallbackType(MapStateCallback);
        static readonly Interop.UwUpdateCallbackType UpdateDelegate = new Interop.UwUpdateCallbackType(UpdateCallback);
        static readonly Interop.UwShootingCallbackType ShootingDelegate = new Interop.UwShootingCallbackType(ShootingCallback);
        static readonly Interop.UwExplosionsCallbackType ExplosionsDelegate = new Interop.UwExplosionsCallbackType(ExplosionsCallback);
        static readonly Interop.UwForceEliminatedCallbackType ForceEliminatedDelegate = new Interop.UwForceEliminatedCallbackType(ForceEliminatedCallback);
        static readonly Interop.UwChatCallbackType ChatDelegate = new Interop.UwChatCallbackType(ChatCallback);

        static void ExceptionCallback([MarshalAs(UnmanagedType.LPStr)] string message)
        {
            Console.WriteLine("exception: " + message);
            if (System.Diagnostics.Debugger.IsAttached)
                System.Diagnostics.Debugger.Break();
        }

        static void ConnectionStateCallback(ConnectionStateEnum state)
        {
            if (ConnectionStateChanged != null)
                ConnectionStateChanged(null, state);
        }

        static void GameStateCallback(GameStateEnum state)
        {
            if (GameStateChanged != null)
                GameStateChanged(null, state);
        }

        static void MapStateCallback(MapStateEnum state)
        {
            if (MapStateChanged != null)
                MapStateChanged(null, state);
        }

        static void UpdateCallback(bool stepping)
        {
            if (Updating != null)
                Updating(null, stepping);
        }

        static void ShootingCallback(ref ShootingArray data)
        {
            if (Shooting == null)
                return;
            ShootingData[] arr = new ShootingData[data.count];
            int size = Marshal.SizeOf(typeof(ShootingData));
            for (int i = 0; i < data.count; i++)
            {
                IntPtr currentPtr = IntPtr.Add(data.data, i * size);
                arr[i] = Marshal.PtrToStructure<ShootingData>(currentPtr);
            }
            Shooting(null, arr);
        }

        static void ExplosionsCallback(ref ExplosionsArray data)
        {
            if (Explosions == null)
                return;
            ExplosionData[] arr = new ExplosionData[data.count];
            int size = Marshal.SizeOf(typeof(ExplosionData));
            for (int i = 0; i < data.count; i++)
            {
                IntPtr currentPtr = IntPtr.Add(data.data, i * size);
                arr[i] = Marshal.PtrToStructure<ExplosionData>(currentPtr);
            }
            Explosions(null, arr);
        }

        static void ForceEliminatedCallback(uint force)
        {
            if (ForceEliminated == null)
                return;
            ForceEliminated(null, force);
        }

        static void ChatCallback(string msg, uint sender, ChatTargetFLags flags)
        {
            if (ChatReceived == null)
                return;
            ChatMessage c = new ChatMessage();
            c.Message = msg;
            c.Sender = sender;
            c.Flags = flags;
            ChatReceived(null, c);
        }


        static Events()
        {
            AppDomain.CurrentDomain.ProcessExit += Destructor;
            Interop.uwInitialize(Interop.UW_VERSION);
            Interop.uwInitializeConsoleLogger();

            Interop.uwSetExceptionCallback(ExceptionDelegate);
            Interop.uwSetConnectionStateCallback(ConnectionStateDelegate);
            Interop.uwSetGameStateCallback(GameStateDelegate);
            Interop.uwSetMapStateCallback(MapStateDelegate);
            Interop.uwSetUpdateCallback(UpdateDelegate);
            Interop.uwSetShootingCallback(ShootingDelegate);
            Interop.uwSetExplosionsCallback(ExplosionsDelegate);
            Interop.uwSetForceEliminatedCallback(ForceEliminatedDelegate);
            Interop.uwSetChatCallback(ChatDelegate);

            // make sure that others register their callbacks too (call any method)
            Prototypes.All();
            Map.Positions();
            World.Entities();
            UwapiTasks.Init();
        }

        static void Destructor(object sender, EventArgs e)
        {
            Interop.uwDeinitialize();
        }
    }

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
