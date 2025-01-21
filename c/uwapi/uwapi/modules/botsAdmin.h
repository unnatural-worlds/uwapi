#ifndef unnatural_uwapi_admin_h_kjh7r8se
#define unnatural_uwapi_admin_h_kjh7r8se

#include "common.h"

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef UNNATURAL_BOTS

	UNNATURAL_API uint64 uwGetLobbyId(void);
	UNNATURAL_API uint64 uwGetUserId(void);
	UNNATURAL_API uint16 uwGetServerPort(void);
	UNNATURAL_API void uwAdminSetMapSelection(const char *path);
	UNNATURAL_API void uwAdminStartGame(void);
	UNNATURAL_API void uwAdminTerminateGame(void);
	UNNATURAL_API void uwAdminSetGameSpeed(float speed);
	UNNATURAL_API void uwAdminSetWeatherSpeed(float speed, float offset);
	UNNATURAL_API void uwAdminAddAi(void);
	UNNATURAL_API void uwAdminKickPlayer(uint32 player);
	UNNATURAL_API void uwAdminPlayerSetAdmin(uint32 player, bool admin);
	UNNATURAL_API void uwAdminPlayerSetName(uint32 player, const char *name);
	UNNATURAL_API void uwAdminPlayerJoinForce(uint32 player, uint32 force);
	UNNATURAL_API void uwAdminForceJoinTeam(uint32 force, uint32 team);
	UNNATURAL_API void uwAdminForceSetColor(uint32 force, float r, float g, float b);
	UNNATURAL_API void uwAdminSendSuggestedCameraFocus(uint32 position);
	UNNATURAL_API void uwAdminSendChat(const char *msg, UwChatTargetFlags flags, uint32 targetId);

#endif

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_admin_h_kjh7r8se
