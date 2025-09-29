namespace Unnatural
{
    using PingEnum = Interop.UwPingEnum;
    using PlayerAiConfig = Interop.UwPlayerAiConfigComponent;

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

        public static void SetGameConfig(Interop.UwGameConfig cfg)
        {
            Interop.uwAdminSetGameConfig(ref cfg);
        }

        public static void StartGame()
        {
            Interop.uwAdminStartGame();
        }

        public static void TerminateGame()
        {
            Interop.uwAdminTerminateGame();
        }

        public static void PauseGame(bool pause)
        {
            Interop.uwAdminPauseGame(pause);
        }

        public static void SkipCutscene()
        {
            Interop.uwAdminSkipCutscene();
        }

        public static void AddAi(uint intendedRace = 0, float difficulty = 0)
        {
            Interop.uwAdminAddAi(intendedRace, difficulty);
        }

        public static void KickPlayer(uint playerId)
        {
            Interop.uwAdminKickPlayer(playerId);
        }

        public static void PlayerSetAdmin(uint playerId, bool admin)
        {
            Interop.uwAdminPlayerSetAdmin(playerId, admin);
        }

        public static void PlayerSetName(uint playerId, string name)
        {
            Interop.uwAdminPlayerSetName(playerId, name);
        }

        public static void PlayerAiConfig(uint playerId, PlayerAiConfig config)
        {
            Interop.uwAdminPlayerAiConfig(playerId, ref config);
        }

        public static void PlayerJoinForce(uint playerId, uint forceId)
        {
            Interop.uwAdminPlayerJoinForce(playerId, forceId);
        }

        public static void ForceJoinTeam(uint forceId, uint team)
        {
            Interop.uwAdminForceJoinTeam(forceId, team);
        }

        public static void ForceSetColor(uint forceId, float r, float g, float b)
        {
            Interop.uwAdminForceSetColor(forceId, r, g, b);
        }

        public static void ForceSetRace(uint forceId, uint raceProto)
        {
            Interop.uwAdminForceSetRace(forceId, raceProto);
        }

        public static void SendSuggestedCameraFocus(uint position)
        {
            Interop.uwAdminSendSuggestedCameraFocus(position);
        }

        public static void SetAutomaticSuggestedCameraFocus(bool enabled)
        {
            Interop.uwAdminSetAutomaticSuggestedCameraFocus(enabled);
        }

        public static void SendChatMessageToEveryone(string msg)
        {
            Interop.uwAdminSendChatMessageToEveryone(msg);
        }

        public static void SendChatMessageToPlayer(string msg, uint id)
        {
            Interop.uwAdminSendChatMessageToPlayer(msg, id);
        }

        public static void SendChatCommand(string msg)
        {
            Interop.uwAdminSendChatCommand(msg);
        }

        public static void SendPing(uint position, PingEnum ping, uint id)
        {
            Interop.uwAdminSendPing(position, ping, id);
        }
    }
}
