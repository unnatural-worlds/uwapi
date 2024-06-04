#ifndef unnatural_uwapi_commands_h_rd5kgz4huf
#define unnatural_uwapi_commands_h_rd5kgz4huf

#include "common.h"

#ifdef __cplusplus
extern "C"
{
#endif

	// initialization

	const uint32 UW_VERSION = 14;
	UNNATURAL_API void uwInitialize(uint32 version);

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

	// entities

	UNNATURAL_API void uwModifiedEntities(UwIds *data);

	// constructions

	UNNATURAL_API bool uwTestConstructionPlacement(uint32 constructionPrototype, uint32 position);
	UNNATURAL_API uint32 uwFindConstructionPlacement(uint32 constructionPrototype, uint32 position);

	// orders

	typedef struct UwOrder
	{
		uint32 entity;
		uint32 position;
		uint8 order;
		uint8 priority;
	} UwOrder;
	UNNATURAL_API void uwOrder(uint32 unit, const UwOrder *data);
	typedef struct UwOrders
	{
		const UwOrder *orders;
		uint32 count;
	} UwOrders;
	UNNATURAL_API void uwOrders(uint32 unit, UwOrders *data);

	// commands

	UNNATURAL_API void uwCommandSelfDestruct(uint32 unit);
	UNNATURAL_API void uwCommandPlaceConstruction(uint32 proto, uint32 position, float yaw);
	UNNATURAL_API void uwCommandSetRecipe(uint32 unit, uint32 recipe);
	UNNATURAL_API void uwCommandLoad(uint32 unit, uint32 resourceType);
	UNNATURAL_API void uwCommandUnload(uint32 unit);
	UNNATURAL_API void uwCommandMove(uint32 unit, uint32 position, float yaw);
	UNNATURAL_API void uwCommandAim(uint32 unit, uint32 target);
	UNNATURAL_API void uwCommandRenounceControl(uint32 unit);

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_commands_h_rd5kgz4huf