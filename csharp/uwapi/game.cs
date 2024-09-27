using System;
using System.Runtime.InteropServices;

namespace Unnatural
{
    using ConnectionStateEnum = Interop.UwConnectionStateEnum;
    using GameStateEnum = Interop.UwGameStateEnum;
    using MapStateEnum = Interop.UwMapStateEnum;
    using ShootingData = Interop.UwShootingData;
    using ShootingArray = Interop.UwShootingArray;

    public static class Game
    {
        public static event EventHandler<ConnectionStateEnum> ConnectionStateChanged;
        public static event EventHandler<GameStateEnum> GameStateChanged;
        public static event EventHandler<MapStateEnum> MapStateChanged;
        public static event EventHandler<bool> Updating;
        public static event EventHandler<ShootingData[]> Shooting;

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

        public static void SetPlayerColor(float r, float g, float b) // [0 .. 1]
        {
            Interop.uwSetPlayerColor(r, g, b);
        }

        public static void SetConnectStartGui(bool startGui, string extraParams = "--observer 1")
        {
            Interop.uwSetConnectStartGui(startGui, extraParams);
        }

        public static void SetConnectAsObserver(bool observer)
        {
            Interop.uwSetConnectAsObserver(observer);
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

        public static void ConnectNewServer(uint visibility = 0, string name = "", string extraParams = "")
        {
            Interop.uwConnectNewServer(visibility, name, extraParams);
        }

        // returns false if no data for reconnect are available
        // returns true if a reconnect was attempted (irrespective of whether actual connection was established)
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

        static readonly Interop.UwExceptionCallbackType ExceptionDelegate = new Interop.UwExceptionCallbackType(ExceptionCallback);
        static readonly Interop.UwLogCallbackType LogDelegate = new Interop.UwLogCallbackType(LogCallback);
        static readonly Interop.UwConnectionStateCallbackType ConnectionStateDelegate = new Interop.UwConnectionStateCallbackType(ConnectionStateCallback);
        static readonly Interop.UwGameStateCallbackType GameStateDelegate = new Interop.UwGameStateCallbackType(GameStateCallback);
        static readonly Interop.UwMapStateCallbackType MapStateDelegate = new Interop.UwMapStateCallbackType(MapStateCallback);
        static readonly Interop.UwUpdateCallbackType UpdateDelegate = new Interop.UwUpdateCallbackType(UpdateCallback);
        static readonly Interop.UwShootingCallbackType ShootingDelegate = new Interop.UwShootingCallbackType(ShootingCallback);
        static uint tick;

        static void ExceptionCallback([MarshalAs(UnmanagedType.LPStr)] string message)
        {
            Console.WriteLine("exception: " + message);
            if (System.Diagnostics.Debugger.IsAttached)
                System.Diagnostics.Debugger.Break();
        }

        static void LogCallback(ref Interop.UwLogCallback data)
        {
            Console.WriteLine(Marshal.PtrToStringAnsi(data.message));
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

        static Game()
        {
            AppDomain.CurrentDomain.ProcessExit += Destructor;

            Interop.uwInitialize(Interop.UW_VERSION);
            Interop.uwSetExceptionCallback(ExceptionDelegate);
            Interop.uwSetLogCallback(LogDelegate);
            Interop.uwSetConnectionStateCallback(ConnectionStateDelegate);
            Interop.uwSetGameStateCallback(GameStateDelegate);
            Interop.uwSetMapStateCallback(MapStateDelegate);
            Interop.uwSetUpdateCallback(UpdateDelegate);
            Interop.uwSetShootingCallback(ShootingDelegate);

            // make sure that others register their callbacks too
            Prototypes.All();
            Map.Positions();
            World.Entities();
        }

        static void Destructor(object sender, EventArgs e)
        {
            Interop.uwDeinitialize();
        }
    }
}
