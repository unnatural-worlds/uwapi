using System;
using System.Runtime.InteropServices;

namespace Unnatural
{
    using ShootingData = Interop.UwShootingData;

    public static class Game
    {
        public static event EventHandler Preparing;
        public static event EventHandler Updating;
        public static event EventHandler<uint> Stepping;
        public static event EventHandler Finished;
        public static event EventHandler<ShootingData> Shooting;

        public static void SetName(string name)
        {
            Interop.uwSetPlayerName(name);
        }

        public static void ConnectLan(ulong timeoutMicroseconds)
        {
            Interop.uwConnectFindLan(timeoutMicroseconds);
        }

        public static void ConnectDirect(string address, ushort port)
        {
            Interop.uwConnectDirect(address, port);
        }

        public static void ConnectLobbyId(ulong lobbyId)
        {
            Interop.uwConnectLobbyId(lobbyId);
        }

        public static void StartNewServer(string mapPath)
        {
            Interop.uwConnectNewServer(mapPath);
        }

        static readonly Interop.UwExceptionCallbackType ExceptionDelegate = new Interop.UwExceptionCallbackType(ExceptionCallback);
        static readonly Interop.UwLogCallbackType LogDelegate = new Interop.UwLogCallbackType(LogCallback);
        static readonly Interop.UwStateCallbackType ConnectionStateDelegate = new Interop.UwStateCallbackType(ConnectionStateCallback);
        static readonly Interop.UwStateCallbackType GameStateDelegate = new Interop.UwStateCallbackType(GameStateCallback);
        static readonly Interop.UwUpdateCallbackType UpdateDelegate = new Interop.UwUpdateCallbackType(UpdateCallback);
        static readonly Interop.UwShootingCallbackType ShootingDelegate = new Interop.UwShootingCallbackType(ShootingCallback);

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

        static void ConnectionStateCallback(uint state)
        {
            Console.WriteLine("connection state: " + state);
        }

        static void GameStateCallback(uint state)
        {
            Console.WriteLine("game state: " + state);
            if (state == 2) // preparation
                Preparing(null, null);
            if (state == 4) // finish
                Finished(null, null);
        }

        static void UpdateCallback(uint tick, bool stepping)
        {
            Updating(null, null);
            if (stepping)
                Stepping(null, tick);
        }

        static void ShootingCallback(ref ShootingData data)
        {
            Shooting(null, data);
        }

        static Game()
        {
            AppDomain.CurrentDomain.ProcessExit += Destructor;

            Interop.uwInitialize(Interop.UW_VERSION);
            Interop.uwSetExceptionCallback(ExceptionDelegate);
            Interop.uwSetLogCallback(LogDelegate);
            Interop.uwSetConnectionStateCallback(ConnectionStateDelegate);
            Interop.uwSetGameStateCallback(GameStateDelegate);
            Interop.uwSetUpdateCallback(UpdateDelegate);
            Interop.uwSetShootingCallback(ShootingDelegate);

            // make sure that others register their callbacks too
            Prototypes.All();
            Map.Positions();
            World.Entities();
        }

        static void Destructor(object sender, EventArgs e)
        {
            Interop.uwSetShootingCallback(null);
            Interop.uwSetUpdateCallback(null);
            Interop.uwSetGameStateCallback(null);
            Interop.uwSetConnectionStateCallback(null);
            Interop.uwSetLogCallback(null);
            Interop.uwSetExceptionCallback(null);
        }
    }
}
