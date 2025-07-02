#ifndef unnatural_uwapi_game_h_we56rs4dcjq
#define unnatural_uwapi_game_h_we56rs4dcjq

#include "common.h"

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef UNNATURAL_BOTS

#endif

	// game state

	typedef enum UwGameStateEnum
	{
		UwGameStateEnum_None = 0,
		UwGameStateEnum_Session = 1,
		UwGameStateEnum_Preparation = 2,
		UwGameStateEnum_Starting = 3,
		UwGameStateEnum_Game = 4,
		UwGameStateEnum_Pause = 5,
		UwGameStateEnum_CutscenePaused = 6,
		UwGameStateEnum_CutsceneRunning = 7,
		UwGameStateEnum_Finish = 8,
	} UwGameStateEnum;
#ifdef UNNATURAL_BOTS
	typedef void (*UwGameStateCallbackType)(UwGameStateEnum state);
	UNNATURAL_API void uwSetGameStateCallback(UwGameStateCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwGameStateCallback(UwGameStateEnum state);
#endif
	UNNATURAL_API UwGameStateEnum uwGameState(void);

	UNNATURAL_API uint32 uwGameTick(void);

	// update callback

#ifdef UNNATURAL_BOTS
	typedef void (*UwUpdateCallbackType)(bool stepping);
	UNNATURAL_API void uwSetUpdateCallback(UwUpdateCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwUpdateCallback(bool stepping);
#endif

	// shooting callback

	typedef struct UwShootingUnit
	{
		uint32 position;
		uint32 force;
		uint32 prototype;
		uint32 id; // beware, it may have expired
	} UwShootingUnit;
	typedef struct UwShootingData
	{
		UwShootingUnit shooter;
		UwShootingUnit target;
	} UwShootingData;
	typedef struct UwShootingArray
	{
		UNNATURAL_POINTER(const UwShootingData *) data;
		uint32 count;
	} UwShootingArray;
#ifdef UNNATURAL_BOTS
	typedef void (*UwShootingCallbackType)(const UwShootingArray *data);
	UNNATURAL_API void uwSetShootingCallback(UwShootingCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwShootingCallback(const UwShootingArray *data);
#endif

	// explosions callback

	typedef struct UwExplosionData
	{
		uint32 position;
		uint32 force;
		uint32 prototype;
		uint32 id; // beware, it is expired
	} UwExplosionData;
	typedef struct UwExplosionsArray
	{
		UNNATURAL_POINTER(const UwExplosionData *) data;
		uint32 count;
	} UwExplosionsArray;
#ifdef UNNATURAL_BOTS
	typedef void (*UwExplosionsCallbackType)(const UwExplosionsArray *data);
	UNNATURAL_API void uwSetExplosionsCallback(UwExplosionsCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwExplosionsCallback(const UwExplosionsArray *data);
#endif

	// force eliminated callback

#ifdef UNNATURAL_BOTS
	typedef void (*UwForceEliminatedCallbackType)(uint32 id);
	UNNATURAL_API void uwSetForceEliminatedCallback(UwForceEliminatedCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwForceEliminatedCallback(uint32 id);
#endif

	// chat

#ifdef UNNATURAL_BOTS
	typedef void (*UwChatCallbackType)(const char *msg, uint32 sender, UwChatTargetFlags flags);
	UNNATURAL_API void uwSetChatCallback(UwChatCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwChatCallback(const char *msg, uint32 sender, UwChatTargetFlags flags);
#endif

	// tasks callback

	typedef enum UwTaskTypeEnum
	{
		UwTaskTypeEnum_None = 0,
		UwTaskTypeEnum_UnitPathfinding = 1,
		UwTaskTypeEnum_ClustersDistances = 2,
	} UwTaskTypeEnum;

#ifdef UNNATURAL_BOTS
	typedef void (*UwTaskCompletedCallbackType)(uint64 taskUserData, UwTaskTypeEnum type);
	UNNATURAL_API void uwSetTaskCompletedCallback(UwTaskCompletedCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwTaskCompletedCallback(uint64 taskUserData, UwTaskTypeEnum type);
#endif

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_game_h_we56rs4dcjq
