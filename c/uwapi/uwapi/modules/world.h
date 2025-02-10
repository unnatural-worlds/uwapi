#ifndef unnatural_uwapi_worlds_h_dcfgh41dr5fsdtg
#define unnatural_uwapi_worlds_h_dcfgh41dr5fsdtg

#include "common.h"

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef UNNATURAL_BOTS
	typedef struct UwEntity UwEntity;
	typedef UwEntity *UwEntityPtr;
	UNNATURAL_API UwEntityPtr uwEntityPointer(uint32 id);
	UNNATURAL_API uint32 uwEntityId(UwEntityPtr entity);
	UNNATURAL_API void uwModifiedEntities(UwIds *data);
#endif

#ifdef UNNATURAL_SCRIPTS
	typedef uint32 UwEntityPtr;
#endif

	UNNATURAL_API void uwAllEntities(UwIds *data);
	UNNATURAL_API bool uwEntityExists(uint32 id);

	typedef struct UwProtoComponent
	{
		uint32 proto;
	} UwProtoComponent;
	UNNATURAL_API bool uwFetchProtoComponent(UwEntityPtr entity, UwProtoComponent *data);

	typedef struct UwOwnerComponent
	{
		uint32 force;
	} UwOwnerComponent;
	UNNATURAL_API bool uwFetchOwnerComponent(UwEntityPtr entity, UwOwnerComponent *data);

	typedef struct UwControllerComponent
	{
		uint32 player;
		uint32 timestamp;
	} UwControllerComponent;
	UNNATURAL_API bool uwFetchControllerComponent(UwEntityPtr entity, UwControllerComponent *data);

	typedef struct UwPositionComponent
	{
		uint32 position;
		float yaw;
	} UwPositionComponent;
	UNNATURAL_API bool uwFetchPositionComponent(UwEntityPtr entity, UwPositionComponent *data);

	typedef enum UwUnitStateFlags
	{
		UwUnitStateFlags_None = 0,
		UwUnitStateFlags_Shooting = 1 << 0,
		UwUnitStateFlags_Processing = 1 << 1, // processing recipe
		UwUnitStateFlags_Rebuilding = 1 << 2, // changing recipe
		UwUnitStateFlags_Stalling = 1 << 3, // usually due to maximumProcessingOutput
	} UwUnitStateFlags;
	typedef struct UwUnitComponent
	{
		UwUnitStateFlags state;
		uint32 killCount;
	} UwUnitComponent;
	UNNATURAL_API bool uwFetchUnitComponent(UwEntityPtr entity, UwUnitComponent *data);

	typedef struct UwLifeComponent
	{
		sint32 life;
	} UwLifeComponent;
	UNNATURAL_API bool uwFetchLifeComponent(UwEntityPtr entity, UwLifeComponent *data);

	typedef struct UwMoveComponent
	{
		uint32 posStart;
		uint32 posEnd;
		uint32 tickStart;
		uint32 tickEnd;
		float yawStart;
		float yawEnd;
	} UwMoveComponent;
	UNNATURAL_API bool uwFetchMoveComponent(UwEntityPtr entity, UwMoveComponent *data);

	typedef struct UwAimComponent
	{
		uint32 target;
	} UwAimComponent;
	UNNATURAL_API bool uwFetchAimComponent(UwEntityPtr entity, UwAimComponent *data);

	typedef struct UwRecipeComponent
	{
		uint32 recipe;
	} UwRecipeComponent;
	UNNATURAL_API bool uwFetchRecipeComponent(UwEntityPtr entity, UwRecipeComponent *data);

	typedef struct UwUpdateTimestampComponent
	{
		uint32 timestamp;
	} UwUpdateTimestampComponent;
	UNNATURAL_API bool uwFetchUpdateTimestampComponent(UwEntityPtr entity, UwUpdateTimestampComponent *data);

	typedef struct UwRecipeStatisticsComponent
	{
		uint32 timestamps[3];
		uint32 completed;
	} UwRecipeStatisticsComponent;
	UNNATURAL_API bool uwFetchRecipeStatisticsComponent(UwEntityPtr entity, UwRecipeStatisticsComponent *data);

	typedef struct UwPriorityComponent
	{
		UwPriorityEnum priority;
	} UwPriorityComponent;
	UNNATURAL_API bool uwFetchPriorityComponent(UwEntityPtr entity, UwPriorityComponent *data);

	typedef struct UwAmountComponent
	{
		uint32 amount;
	} UwAmountComponent;
	UNNATURAL_API bool uwFetchAmountComponent(UwEntityPtr entity, UwAmountComponent *data);

	typedef struct UwAttachmentComponent
	{
		uint32 target;
	} UwAttachmentComponent;
	UNNATURAL_API bool uwFetchAttachmentComponent(UwEntityPtr entity, UwAttachmentComponent *data);

	typedef enum UwPlayerStateFlags
	{
		UwPlayerStateFlags_None = 0,
		UwPlayerStateFlags_Loaded = 1 << 0,
		UwPlayerStateFlags_Pause = 1 << 1,
		UwPlayerStateFlags_Disconnected = 1 << 2,
		UwPlayerStateFlags_Admin = 1 << 3,
	} UwPlayerStateFlags;
	typedef enum UwPlayerConnectionClassEnum
	{
		UwPlayerConnectionClassEnum_None = 0,
		UwPlayerConnectionClassEnum_Computer = 1,
		UwPlayerConnectionClassEnum_VirtualReality = 2,
		UwPlayerConnectionClassEnum_Robot = 3,
		UwPlayerConnectionClassEnum_UwApi = 4,
	} UwPlayerConnectionClassEnum;
	typedef struct UwPlayerComponent
	{
		char name[28];
		uint32 nameLength;
		uint64 steamUserId;
		uint32 force;
		float progress;
		uint32 ping;
		UwPlayerStateFlags state;
		UwPlayerConnectionClassEnum playerConnectionClass;
	} UwPlayerComponent;
	UNNATURAL_API bool uwFetchPlayerComponent(UwEntityPtr entity, UwPlayerComponent *data);

	typedef enum UwForceStateFlags
	{
		UwForceStateFlags_None = 0,
		UwForceStateFlags_Winner = 1 << 0,
		UwForceStateFlags_Defeated = 1 << 1,
		UwForceStateFlags_Disconnected = 1 << 2,
	} UwForceStateFlags;
	typedef struct UwForceComponent
	{
		float color[3];
		uint64 score;
		uint32 killCount;
		uint32 lossCount;
		uint32 finishTimestamp;
		uint32 intendedTeam;
		uint32 intendedRace;
		UwForceStateFlags state;
	} UwForceComponent;
	UNNATURAL_API bool uwFetchForceComponent(UwEntityPtr entity, UwForceComponent *data);

	typedef struct UwForceDetailsComponent
	{
		uint64 killValue;
		uint64 lossValue;
		uint32 startingPosition;
		uint32 race;
	} UwForceDetailsComponent;
	UNNATURAL_API bool uwFetchForceDetailsComponent(UwEntityPtr entity, UwForceDetailsComponent *data);

	typedef struct UwForeignPolicyComponent
	{
		uint32 forces[2];
		UwForeignPolicyEnum policy;
	} UwForeignPolicyComponent;
	UNNATURAL_API bool uwFetchForeignPolicyComponent(UwEntityPtr entity, UwForeignPolicyComponent *data);

	typedef struct UwDiplomacyProposalComponent
	{
		uint32 offeror;
		uint32 offeree;
		UwForeignPolicyEnum proposal;
	} UwDiplomacyProposalComponent;
	UNNATURAL_API bool uwFetchDiplomacyProposalComponent(UwEntityPtr entity, UwDiplomacyProposalComponent *data);

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_worlds_h_dcfgh41dr5fsdtg
