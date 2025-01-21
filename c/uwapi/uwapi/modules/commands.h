#ifndef unnatural_uwapi_commands_h_xcfhgvr78tb
#define unnatural_uwapi_commands_h_xcfhgvr78tb

#include "common.h"

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef UNNATURAL_BOTS

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
		UNNATURAL_POINTER(const UwOrder *) orders;
		uint32 count;
	} UwOrders;
	UNNATURAL_API void uwOrders(uint32 unit, UwOrders *data);

	typedef enum UwPathStateEnum
	{
		UwPathStateEnum_None = 0,
		UwPathStateEnum_Searching = 1,
		UwPathStateEnum_Impossible = 2,
		UwPathStateEnum_NotFound = 3,
		UwPathStateEnum_Recompute = 4,
		UwPathStateEnum_Found = 5,
		UwPathStateEnum_Finished = 6,
	} UwPathStateEnum;
	UNNATURAL_API UwPathStateEnum uwPathState(uint32 unit);

	UNNATURAL_API void uwCommandPlaceConstruction(uint32 constructionProto, uint32 position, float yaw, uint32 recipeProto, UwPriorityEnum priority); // recipeProto may be 0
	UNNATURAL_API void uwCommandSetRecipe(uint32 unitOrConstruction, uint32 recipeProto);
	UNNATURAL_API void uwCommandSetPriority(uint32 unitOrConstruction, UwPriorityEnum priority);
	UNNATURAL_API void uwCommandLoad(uint32 unit, uint32 resourceType);
	UNNATURAL_API void uwCommandUnload(uint32 unit);
	UNNATURAL_API void uwCommandMove(uint32 unit, uint32 position, float yaw); // neighboring position only
	UNNATURAL_API void uwCommandAim(uint32 unit, uint32 target);
	UNNATURAL_API void uwCommandRenounceControl(uint32 unitOrConstruction);
	UNNATURAL_API void uwCommandSelfDestruct(uint32 entity);

#endif

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_commands_h_xcfhgvr78tb
