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

        public static void SetPlayerName(string name)
        {
            Interop.uwSetPlayerName(name);
        }

        public static void SetPlayerColor(float r, float g, float b)
        {
            Interop.uwSetPlayerColor(r, g, b);
        }

        public static void SetStartGui(bool startGui, string extraParams = "")
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

        public static void ConnectNewServer(string extraParams = "")
        {
            Interop.uwConnectNewServer(extraParams);
        }

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
            Console.WriteLine("connection state: " + state);
            if (ConnectionStateChanged != null)
                ConnectionStateChanged(null, state);
        }

        static void GameStateCallback(GameStateEnum state)
        {
            Console.WriteLine("game state: " + state);
            if (GameStateChanged != null)
                GameStateChanged(null, state);
        }

        static void MapStateCallback(MapStateEnum state)
        {
            Console.WriteLine("map state: " + state);
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
