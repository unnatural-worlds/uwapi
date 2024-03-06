#ifndef unnatural_uwapi_commands_h_rd5kgz4huf
#define unnatural_uwapi_commands_h_rd5kgz4huf

#include "core.h"

#ifdef __cplusplus
extern "C"
{
#endif

	// commands

	UNNATURAL_API void uwCommandSelfDestruct(uint32 unit);
	UNNATURAL_API void uwCommandPlaceConstruction(uint32 proto, uint32 position, float yaw);
	UNNATURAL_API void uwCommandSetRecipe(uint32 unit, uint32 recipe);
	UNNATURAL_API void uwCommandLoadAll(uint32 unit, uint32 resourceType);
	UNNATURAL_API void uwCommandUnloadAll(uint32 unit);
	UNNATURAL_API void uwCommandMove(uint32 unit, uint32 position, float yaw);
	UNNATURAL_API void uwCommandAim(uint32 unit, uint32 target);
	UNNATURAL_API void uwCommandRenounceControl(uint32 unit);

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

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_commands_h_rd5kgz4huf
