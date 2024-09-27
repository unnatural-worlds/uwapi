#ifndef unnatural_uwapi_commands_h_rd5kgz4huf
#define unnatural_uwapi_commands_h_rd5kgz4huf

#include "common.h"

#ifdef __cplusplus
extern "C"
{
#endif

	// initialization

	static const uint32 UW_VERSION = 22;
	UNNATURAL_API void uwInitialize(uint32 version);
	UNNATURAL_API void uwDeinitialize(void);

	typedef void (*UwExceptionCallbackType)(const char *message);
	UNNATURAL_API void uwSetExceptionCallback(UwExceptionCallbackType callback);

	typedef enum UwSeverityEnum
	{
		UwSeverityEnum_Note = 0,
		UwSeverityEnum_Hint = 1,
		UwSeverityEnum_Warning = 2,
		UwSeverityEnum_Info = 3,
		UwSeverityEnum_Error = 4,
		UwSeverityEnum_Critical = 5,
	} UwSeverityEnum;
	typedef struct UwLogCallback
	{
		const char *message;
		const char *component;
		UwSeverityEnum severity;
	} UwLogCallback;
	typedef void (*UwLogCallbackType)(const UwLogCallback *data);
	UNNATURAL_API void uwSetLogCallback(UwLogCallbackType callback);
	UNNATURAL_API void uwLog(UwSeverityEnum severity, const char *message);

	typedef struct UwAssistConfig
	{
		bool logistics;
		bool aiming;
		bool fighting;
		bool retaliations;
	} UwAssistConfig;
	UNNATURAL_API void uwSetAssistConfig(const UwAssistConfig *config);

	UNNATURAL_API void uwSetPlayerName(const char *name);
	UNNATURAL_API void uwSetPlayerColor(float r, float g, float b); // [0 .. 1]
	UNNATURAL_API void uwSetConnectStartGui(bool enabled, const char *extraCmdParams);
	UNNATURAL_API void uwSetConnectAsObserver(bool observer);

	UNNATURAL_API bool uwConnectFindLan(uint64 timeoutMicroseconds);
	UNNATURAL_API void uwConnectDirect(const char *address, uint16 port);
	UNNATURAL_API void uwConnectLobbyId(uint64 lobbyId);
	UNNATURAL_API void uwConnectNewServer(uint32 visibility, const char *name, const char *extraCmdParams);
	UNNATURAL_API bool uwTryReconnect(void);
	UNNATURAL_API void uwDisconnect(void);

	// game state and callbacks

	typedef enum UwConnectionStateEnum
	{
		UwConnectionStateEnum_None = 0,
		UwConnectionStateEnum_Connecting = 1,
		UwConnectionStateEnum_Connected = 2,
		UwConnectionStateEnum_Disconnecting = 3,
		UwConnectionStateEnum_Error = 4,
	} UwConnectionStateEnum;
	typedef void (*UwConnectionStateCallbackType)(UwConnectionStateEnum state);
	UNNATURAL_API void uwSetConnectionStateCallback(UwConnectionStateCallbackType callback);
	UNNATURAL_API UwConnectionStateEnum uwConnectionState(void);

	typedef enum UwGameStateEnum
	{
		UwGameStateEnum_None = 0,
		UwGameStateEnum_Session = 1,
		UwGameStateEnum_Preparation = 2,
		UwGameStateEnum_Game = 3,
		UwGameStateEnum_Finish = 4,
	} UwGameStateEnum;
	typedef void (*UwGameStateCallbackType)(UwGameStateEnum state);
	UNNATURAL_API void uwSetGameStateCallback(UwGameStateCallbackType callback);
	UNNATURAL_API UwGameStateEnum uwGameState(void);

	typedef enum UwMapStateEnum
	{
		UwMapStateEnum_None = 0,
		UwMapStateEnum_Downloading = 1,
		UwMapStateEnum_Loading = 2,
		UwMapStateEnum_Loaded = 3,
		UwMapStateEnum_Unloading = 4,
		UwMapStateEnum_Error = 5,
	} UwMapStateEnum;
	typedef void (*UwMapStateCallbackType)(UwMapStateEnum state);
	UNNATURAL_API void uwSetMapStateCallback(UwMapStateCallbackType callback);
	UNNATURAL_API UwMapStateEnum uwMapState(void);

	typedef void (*UwUpdateCallbackType)(uint32 tick, bool stepping);
	UNNATURAL_API void uwSetUpdateCallback(UwUpdateCallbackType callback);

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
		const UwShootingData *data;
		uint32 count;
	} UwShootingArray;
	typedef void (*UwShootingCallbackType)(const UwShootingArray *data);
	UNNATURAL_API void uwSetShootingCallback(UwShootingCallbackType callback);

	// my player

	typedef struct UwMyPlayer
	{
		uint32 playerEntityId;
		uint32 forceEntityId;
		bool primaryController;
		bool admin;
	} UwMyPlayer;
	UNNATURAL_API bool uwMyPlayer(UwMyPlayer *data);

	// entities

	UNNATURAL_API void uwModifiedEntities(UwIds *data);

	// constructions

	UNNATURAL_API bool uwTestConstructionPlacement(uint32 constructionProto, uint32 position, uint32 recipeProto); // recipeProto may be 0
	UNNATURAL_API uint32 uwFindConstructionPlacement(uint32 constructionProto, uint32 position, uint32 recipeProto); // recipeProto may be 0

	// orders

	typedef enum UwOrderTypeEnum
	{
		UwOrderTypeEnum_None = 0,
		UwOrderTypeEnum_Stop = 1,
		UwOrderTypeEnum_Guard = 2,
		UwOrderTypeEnum_Run = 3,
		UwOrderTypeEnum_Fight = 4,
		UwOrderTypeEnum_Load = 5,
		UwOrderTypeEnum_Unload = 6,
		UwOrderTypeEnum_SelfDestruct = 7,
	} UwOrderTypeEnum;
	typedef enum UwOrderPriorityFlags
	{
		UwOrderPriorityFlags_None = 0,
		UwOrderPriorityFlags_Assistant = 1 << 0,
		UwOrderPriorityFlags_User = 1 << 1,
		UwOrderPriorityFlags_Enqueue = 1 << 2,
		UwOrderPriorityFlags_Repeat = 1 << 3,
	} UwOrderPriorityFlags;
	typedef struct UwOrder
	{
		uint32 entity;
		uint32 position;
		UwOrderTypeEnum order;
		UwOrderPriorityFlags priority;
	} UwOrder;
	UNNATURAL_API void uwOrder(uint32 unit, const UwOrder *data);
	typedef struct UwOrders
	{
		const UwOrder *orders;
		uint32 count;
	} UwOrders;
	UNNATURAL_API void uwOrders(uint32 unit, UwOrders *data);

	// commands

	UNNATURAL_API void uwCommandPlaceConstruction(uint32 constructionProto, uint32 position, float yaw, uint32 recipeProto, UwPriorityEnum priority); // recipeProto may be 0
	UNNATURAL_API void uwCommandSetRecipe(uint32 unitOrConstruction, uint32 recipe);
	UNNATURAL_API void uwCommandSetPriority(uint32 unitOrConstruction, UwPriorityEnum priority);
	UNNATURAL_API void uwCommandLoad(uint32 unit, uint32 resourceType);
	UNNATURAL_API void uwCommandUnload(uint32 unit);
	UNNATURAL_API void uwCommandMove(uint32 unit, uint32 position, float yaw);
	UNNATURAL_API void uwCommandAim(uint32 unit, uint32 target);
	UNNATURAL_API void uwCommandRenounceControl(uint32 unitOrConstruction);
	UNNATURAL_API void uwCommandSelfDestruct(uint32 entity);

	// admin only

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

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_commands_h_rd5kgz4huf
