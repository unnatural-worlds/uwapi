namespace Unnatural
{
    public static class Admin
    {
        public static ulong GetLobbyId()
        {
            return Interop.uwGetLobbyId();
        }

        public static ulong GetUserId()
        {
            return Interop.uwGetUserId();
        }

        public static ushort GetServerPort()
        {
            return Interop.uwGetServerPort();
        }

        public static void SetMapSelection(string path)
        {
            Interop.uwAdminSetMapSelection(path);
        }

        public static void StartGame()
        {
            Interop.uwAdminStartGame();
        }

        public static void TerminateGame()
        {
            Interop.uwAdminTerminateGame();
        }

        public static void SetGameSpeed(float speed)
        {
            Interop.uwAdminSetGameSpeed(speed);
        }

        public static void SetWeatherSpeed(float speed, float offset)
        {
            Interop.uwAdminSetWeatherSpeed(speed, offset);
        }

        public static void AddAi()
        {
            Interop.uwAdminAddAi();
        }

        public static void KickPlayer(uint player)
        {
            Interop.uwAdminKickPlayer(player);
        }

        public static void PlayerSetAdmin(uint player, bool admin)
        {
            Interop.uwAdminPlayerSetAdmin(player, admin);
        }

        public static void PlayerSetName(uint player, string name)
        {
            Interop.uwAdminPlayerSetName(player, name);
        }

        public static void PlayerJoinForce(uint player, uint force)
        {
            Interop.uwAdminPlayerJoinForce(player, force);
        }

        public static void ForceJoinTeam(uint force, uint team)
        {
            Interop.uwAdminForceJoinTeam(force, team);
        }

        public static void ForceSetColor(uint force, float r, float g, float b)
        {
            Interop.uwAdminForceSetColor(force, r, g, b);
        }

        public static void SendSuggestedCameraFocus(uint position)
        {
            Interop.uwAdminSendSuggestedCameraFocus(position);
        }
    }
}
