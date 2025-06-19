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

    public static class Game
    {
        public static event EventHandler<ConnectionStateEnum> ConnectionStateChanged;
        public static event EventHandler<GameStateEnum> GameStateChanged;
        public static event EventHandler<MapStateEnum> MapStateChanged;
        public static event EventHandler<bool> Updating;
        public static event EventHandler<ShootingData[]> Shooting;
        public static event EventHandler<ExplosionData[]> Explosions;
        public static event EventHandler<uint> ForceEliminated;
        public static event EventHandler<ChatMessage> ChatReceived;

        public static void LogInfo(string msg)
        {
            Interop.uwLog(Interop.UwSeverityEnum.Info, msg);
        }

        public static void LogWarning(string msg)
        {
            Interop.uwLog(Interop.UwSeverityEnum.Warning, msg);
        }

        public static void LogError(string msg)
        {
            Interop.uwLog(Interop.UwSeverityEnum.Error, msg);
        }

        public static void SetPlayerName(string name)
        {
            Interop.uwSetPlayerName(name);
        }

        public static void PlayerJoinForce(uint forceId)
        {
            Interop.uwPlayerJoinForce(forceId);
        }

        public static void SetForceColor(float r, float g, float b) // [0 .. 1]
        {
            Interop.uwSetForceColor(r, g, b);
        }

        public static void SetForceRace(uint raceProto)
        {
            Interop.uwSetForceRace(raceProto);
        }

        public static void ForceJoinTeam(uint team)
        {
            Interop.uwForceJoinTeam(team);
        }

        public static void SetConnectStartGui(bool startGui, string extraParams = "--observer 1")
        {
            Interop.uwSetConnectStartGui(startGui, extraParams);
        }

        public static bool ConnectFindLan(ulong timeoutMicroseconds = 1000000)
        {
            return Interop.uwConnectFindLan(timeoutMicroseconds);
        }

        public static void ConnectDirect(string address, ushort port)
        {
            Interop.uwConnectDirect(address, port);
        }

        public static void ConnectLobbyId(ulong lobbyId)
        {
            Interop.uwConnectLobbyId(lobbyId);
        }

        public static bool ConnectEnvironment()
        {
            return Interop.uwConnectEnvironment();
        }

        public static void ConnectNewServer(uint visibility = 0, string name = "", string extraParams = "")
        {
            Interop.uwConnectNewServer(visibility, name, extraParams);
        }

        // returns false if no data for reconnect are available
        // returns true after a reconnect was attempted (irrespective of whether actual connection has succeded)
        public static bool TryReconnect()
        {
            return Interop.uwTryReconnect();
        }

        public static void Disconnect()
        {
            Interop.uwDisconnect();
        }

        public static ConnectionStateEnum ConnectionState()
        {
            return Interop.uwConnectionState();
        }

        public static GameStateEnum GameState()
        {
            return Interop.uwGameState();
        }

        public static MapStateEnum MapState()
        {
            return Interop.uwMapState();
        }

        public static uint Tick()
        {
            return tick;
        }

        public static Interop.UwPerformanceStatistics PerformanceStatistics()
        {
            Interop.UwPerformanceStatistics data = new Interop.UwPerformanceStatistics();
            Interop.uwPerformanceStatistics(ref data);
            return data;
        }

        public static void PerformanceProfiling(bool enable)
        {
            Interop.uwPerformanceProfiling(enable);
        }

        public static ulong ProfilingEventBegin()
        {
            return Interop.uwProfilingEventBegin();
        }

        public static void ProfilingEventEnd(string name, ulong eventStartTime)
        {
            Interop.uwProfilingEventEnd(name, eventStartTime);
        }

        static readonly Interop.UwExceptionCallbackType ExceptionDelegate = new Interop.UwExceptionCallbackType(ExceptionCallback);
        static readonly Interop.UwConnectionStateCallbackType ConnectionStateDelegate = new Interop.UwConnectionStateCallbackType(ConnectionStateCallback);
        static readonly Interop.UwGameStateCallbackType GameStateDelegate = new Interop.UwGameStateCallbackType(GameStateCallback);
        static readonly Interop.UwMapStateCallbackType MapStateDelegate = new Interop.UwMapStateCallbackType(MapStateCallback);
        static readonly Interop.UwUpdateCallbackType UpdateDelegate = new Interop.UwUpdateCallbackType(UpdateCallback);
        static readonly Interop.UwShootingCallbackType ShootingDelegate = new Interop.UwShootingCallbackType(ShootingCallback);
        static readonly Interop.UwExplosionsCallbackType ExplosionsDelegate = new Interop.UwExplosionsCallbackType(ExplosionsCallback);
        static readonly Interop.UwForceEliminatedCallbackType ForceEliminatedDelegate = new Interop.UwForceEliminatedCallbackType(ForceEliminatedCallback);
        static readonly Interop.UwChatCallbackType ChatDelegate = new Interop.UwChatCallbackType(ChatCallback);
        static uint tick;

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

        static void UpdateCallback(uint tick, bool stepping)
        {
            Game.tick = tick;
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

        static Game()
        {
            AppDomain.CurrentDomain.ProcessExit += Destructor;

            Interop.uwInitialize(Interop.UW_VERSION);
            Interop.uwSetExceptionCallback(ExceptionDelegate);
            Interop.uwInitializeConsoleLogger();
            Interop.uwSetConnectionStateCallback(ConnectionStateDelegate);
            Interop.uwSetGameStateCallback(GameStateDelegate);
            Interop.uwSetMapStateCallback(MapStateDelegate);
            Interop.uwSetUpdateCallback(UpdateDelegate);
            Interop.uwSetShootingCallback(ShootingDelegate);
            Interop.uwSetExplosionsCallback(ExplosionsDelegate);
            Interop.uwSetForceEliminatedCallback(ForceEliminatedDelegate);
            Interop.uwSetChatCallback(ChatDelegate);

            // make sure that others register their callbacks too
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
}
