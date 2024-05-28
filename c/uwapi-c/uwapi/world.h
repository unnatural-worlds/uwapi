#ifndef unnatural_uwapi_components_h_kjsdf58s
#define unnatural_uwapi_components_h_kjsdf58s

#include "core.h"

#ifdef __cplusplus
extern "C"
{
#endif

	// entity

	typedef struct UwEntity UwEntity;
	UNNATURAL_API UwEntity *uwEntityPointer(uint32 id);
	UNNATURAL_API uint32 uwEntityId(UwEntity *entity);
	UNNATURAL_API void uwAllEntities(UwIds *data);
	UNNATURAL_API void uwModifiedEntities(UwIds *data);

	// components

	typedef struct UwProtoComponent
	{
		uint32 proto;
	} UwProtoComponent;
	UNNATURAL_API bool uwFetchProtoComponent(UwEntity *entity, UwProtoComponent *data);

	typedef struct UwOwnerComponent
	{
		uint32 force;
	} UwOwnerComponent;
	UNNATURAL_API bool uwFetchOwnerComponent(UwEntity *entity, UwOwnerComponent *data);

	typedef struct UwControllerComponent
	{
		uint32 player;
		uint32 timestamp;
	} UwControllerComponent;
	UNNATURAL_API bool uwFetchControllerComponent(UwEntity *entity, UwControllerComponent *data);

	typedef struct UwPositionComponent
	{
		uint32 position;
		float yaw;
	} UwPositionComponent;
	UNNATURAL_API bool uwFetchPositionComponent(UwEntity *entity, UwPositionComponent *data);

	typedef struct UwUnitComponent
	{
		uint32 state;
		uint32 killCount;
	} UwUnitComponent;
	UNNATURAL_API bool uwFetchUnitComponent(UwEntity *entity, UwUnitComponent *data);

	typedef struct UwLifeComponent
	{
		sint32 life;
	} UwLifeComponent;
	UNNATURAL_API bool uwFetchLifeComponent(UwEntity *entity, UwLifeComponent *data);

	typedef struct UwMoveComponent
	{
		uint32 posStart;
		uint32 posEnd;
		uint32 tickStart;
		uint32 tickEnd;
		float yawStart;
		float yawEnd;
	} UwMoveComponent;
	UNNATURAL_API bool uwFetchMoveComponent(UwEntity *entity, UwMoveComponent *data);

	typedef struct UwAimComponent
	{
		uint32 target;
	} UwAimComponent;
	UNNATURAL_API bool uwFetchAimComponent(UwEntity *entity, UwAimComponent *data);

	typedef struct UwRecipeComponent
	{
		uint32 recipe;
	} UwRecipeComponent;
	UNNATURAL_API bool uwFetchRecipeComponent(UwEntity *entity, UwRecipeComponent *data);

	typedef struct UwUpdateTimestampComponent
	{
		uint32 timestamp;
	} UwUpdateTimestampComponent;
	UNNATURAL_API bool uwFetchUpdateTimestampComponent(UwEntity *entity, UwUpdateTimestampComponent *data);

	typedef struct UwRecipeStatisticsComponent
	{
		uint32 timestamps[3];
		uint32 completed;
	} UwRecipeStatisticsComponent;
	UNNATURAL_API bool uwFetchRecipeStatisticsComponent(UwEntity *entity, UwRecipeStatisticsComponent *data);

	typedef struct UwAmountComponent
	{
		uint32 amount;
	} UwAmountComponent;
	UNNATURAL_API bool uwFetchAmountComponent(UwEntity *entity, UwAmountComponent *data);

	typedef struct UwAttachmentComponent
	{
		uint32 target;
	} UwAttachmentComponent;
	UNNATURAL_API bool uwFetchAttachmentComponent(UwEntity *entity, UwAttachmentComponent *data);

	typedef struct UwPlayerComponent
	{
		char name[28];
		uint32 nameLength;
		uint64 steamUserId;
		uint32 force;
		float progress;
		uint32 ping;
		uint32 state;
		uint8 playerConnectionClass;
		uint8 dummy[7];
	} UwPlayerComponent;
	UNNATURAL_API bool uwFetchPlayerComponent(UwEntity *entity, UwPlayerComponent *data);

	typedef struct UwForceComponent
	{
		float color[3];
		uint64 score;
		uint32 killCount;
		uint32 lossCount;
		uint32 team;
		uint32 state;
	} UwForceComponent;
	UNNATURAL_API bool uwFetchForceComponent(UwEntity *entity, UwForceComponent *data);

	typedef struct UwForceDetailsComponent
	{
		uint64 killValue;
		uint64 lossValue;
		uint32 startingPosition;
	} UwForceDetailsComponent;
	UNNATURAL_API bool uwFetchForceDetailsComponent(UwEntity *entity, UwForceDetailsComponent *data);

	typedef struct UwForeignPolicyComponent
	{
		uint32 forces[2];
		uint32 policy;
	} UwForeignPolicyComponent;
	UNNATURAL_API bool uwFetchForeignPolicyComponent(UwEntity *entity, UwForeignPolicyComponent *data);

	typedef struct UwDiplomacyProposalComponent
	{
		uint32 offeror;
		uint32 offeree;
		uint32 proposal;
	} UwDiplomacyProposalComponent;
	UNNATURAL_API bool uwFetchDiplomacyProposalComponent(UwEntity *entity, UwDiplomacyProposalComponent *data);

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_components_h_kjsdf58s
