#ifndef unnatural_uwapi_game_h_we56rs4dcjq
#define unnatural_uwapi_game_h_we56rs4dcjq

#include "common.h"

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef UNNATURAL_BOTS

	// my player

	typedef struct UwMyPlayer
	{
		uint32 playerEntityId;
		uint32 forceEntityId;
		bool primaryController;
		bool admin;
	} UwMyPlayer;
	UNNATURAL_API bool uwMyPlayer(UwMyPlayer *data);

	typedef struct UwMyForceStatistics
	{
		uint32 logisticsUnitsIdle;
		uint32 logisticsUnitsTotal;
		uint32 militaryUnitsIdle;
		uint32 militaryUnitsTotal;
		uint32 closestDangerPosition;
		float closestDangerDistance;
	} UwMyForceStatistics;
	UNNATURAL_API void uwMyForceStatistics(UwMyForceStatistics *data);

	typedef struct UwAssistConfig
	{
		bool logistics;
		bool aiming;
		bool fighting;
	} UwAssistConfig;
	UNNATURAL_API void uwSetAssistConfig(const UwAssistConfig *config);

#endif

	// game state

	typedef enum UwGameStateEnum
	{
		UwGameStateEnum_None = 0,
		UwGameStateEnum_Session = 1,
		UwGameStateEnum_Preparation = 2,
		UwGameStateEnum_Game = 3,
		UwGameStateEnum_Finish = 4,
	} UwGameStateEnum;
#ifdef UNNATURAL_BOTS
	typedef void (*UwGameStateCallbackType)(UwGameStateEnum state);
	UNNATURAL_API void uwSetGameStateCallback(UwGameStateCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwGameStateCallback(UwGameStateEnum state);
#endif
	UNNATURAL_API UwGameStateEnum uwGameState(void);

	// update callback

#ifdef UNNATURAL_BOTS
	typedef void (*UwUpdateCallbackType)(uint32 tick, bool stepping);
	UNNATURAL_API void uwSetUpdateCallback(UwUpdateCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwUpdateCallback(uint32 tick, bool stepping);
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

	// chat

#ifdef UNNATURAL_BOTS
	typedef void (*UwChatCallbackType)(const char *msg, uint32 sender, UwChatTargetFlags flags);
	UNNATURAL_API void uwSetChatCallback(UwChatCallbackType callback);
#endif
#ifdef UNNATURAL_SCRIPTS
	UNNATURAL_ENTRY void uwChatCallback(const char *msg, uint32 sender, UwChatTargetFlags flags);
#endif

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_game_h_we56rs4dcjq
