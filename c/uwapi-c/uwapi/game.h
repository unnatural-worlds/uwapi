#ifndef unnatural_uwapi_game_h_xcvh4o5
#define unnatural_uwapi_game_h_xcvh4o5

#include "core.h"

#ifdef __cplusplus
extern "C"
{
#endif

	// initialization

	typedef void (*UwExceptionCallbackType)(const char *message);
	UNNATURAL_API void uwSetExceptionCallback(UwExceptionCallbackType callback);

	typedef struct UwLogCallback
	{
		const char *message;
		const char *component;
		uint32 severity;
	} UwLogCallback;
	typedef void (*UwLogCallbackType)(const UwLogCallback *data);
	UNNATURAL_API void uwSetLogCallback(UwLogCallbackType callback);
	UNNATURAL_API void uwLog(uint32 severity, const char *message);

	UNNATURAL_API void uwSetAssistLogistics(bool enabled);
	UNNATURAL_API void uwSetAssistFighting(bool enabled);

	UNNATURAL_API void uwSetPlayerName(const char *name);
	UNNATURAL_API void uwSetPlayerColor(float r, float g, float b);

	UNNATURAL_API bool uwConnectFindLan(uint64 timeoutMicroseconds);
	UNNATURAL_API void uwConnectDirect(const char *address, uint16 port);
	UNNATURAL_API void uwConnectLobbyId(uint64 lobbyId);
	UNNATURAL_API void uwConnectNewServer(const char *mapPath);

	// game state and callbacks

	typedef void (*UwStateCallbackType)(uint32 state);
	UNNATURAL_API void uwSetConnectionStateCallback(UwStateCallbackType callback);
	UNNATURAL_API uint32 uwConnectionState(void);

	UNNATURAL_API void uwSetGameStateCallback(UwStateCallbackType callback);
	UNNATURAL_API uint32 uwGameState(void);

	typedef void (*UwUpdateCallbackType)(uint32 tick, bool stepping);
	UNNATURAL_API void uwSetUpdateCallback(UwUpdateCallbackType callback);

	typedef struct UwShootingUnit
	{
		uint32 position;
		uint32 force;
		uint32 prototype;
	} UwShootingUnit;
	typedef struct UwShootingData
	{
		UwShootingUnit shooter;
		UwShootingUnit target;
	} UwShootingData;
	typedef void (*UwShootingCallbackType)(const UwShootingData *data);
	UNNATURAL_API void uwSetShootingCallback(UwShootingCallbackType callback);

	// my player

	typedef struct UwMyPlayer
	{
		uint32 playerEntityId;
		uint32 forceEntityId;
		bool primaryController;
	} UwMyPlayer;
	UNNATURAL_API bool uwMyPlayer(UwMyPlayer *data);

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_game_h_xcvh4o5
