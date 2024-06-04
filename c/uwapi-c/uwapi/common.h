#ifndef unnatural_uwapi_common_h_sdr8g4h1u
#define unnatural_uwapi_common_h_sdr8g4h1u

#include <stdbool.h>
#include <stdint.h>

typedef uint8_t uint8;
typedef int8_t sint8;
typedef uint16_t uint16;
typedef int16_t sint16;
typedef uint32_t uint32;
typedef int32_t sint32;
typedef uint64_t uint64;
typedef int64_t sint64;

#ifndef UNNATURAL_API
	#define UNNATURAL_API
#endif // !UNNATURAL_API

#ifdef __cplusplus
extern "C"
{
#endif

	typedef struct UwIds
	{
		const uint32 *ids;
		uint32 count;
	} UwIds;

	// prototypes

	UNNATURAL_API void uwAllPrototypes(UwIds *data);
	UNNATURAL_API uint32 uwPrototypeType(uint32 prototypeId);
	UNNATURAL_API const char *uwPrototypeJson(uint32 prototypeId);
	UNNATURAL_API const char *uwDefinitionsJson(void);

	// map

	typedef struct UwMapInfo
	{
		const char *name;
		const char *guid;
	} UwMapInfo;
	UNNATURAL_API bool uwMapInfo(UwMapInfo *data);

	// tiles

	UNNATURAL_API uint32 uwTilesCount(void);
	typedef struct UwTile
	{
		float position[3];
		float up[3];
		const uint32 *neighborsIndices;
		uint32 neighborsCount;
		uint8 terrain;
		bool border;
	} UwTile;
	UNNATURAL_API void uwTile(uint32 index, UwTile *data);

	// overview

	UNNATURAL_API uint8 uwOverviewFlags(uint32 position);
	UNNATURAL_API void uwOverviewIds(uint32 position, UwIds *data);
	typedef struct UwOverviewExtract
	{
		const uint8 *flags;
		uint32 count;
	} UwOverviewExtract;
	UNNATURAL_API void uwOverviewExtract(UwOverviewExtract *data);

	// map miscellaneous

	UNNATURAL_API void uwAreaRange(float x, float y, float z, float radius, UwIds *data);
	UNNATURAL_API void uwAreaConnected(uint32 position, float radius, UwIds *data);
	UNNATURAL_API void uwAreaNeighborhood(uint32 position, float radius, UwIds *data);
	UNNATURAL_API void uwAreaExtended(uint32 position, float radius, UwIds *data);

	UNNATURAL_API bool uwTestVisible(float x1, float y1, float z1, float x2, float y2, float z2);
	UNNATURAL_API bool uwTestShooting(uint32 shooterPosition, uint32 shooterProto, uint32 targetPosition, uint32 targetProto);
	UNNATURAL_API float uwDistanceLine(float x1, float y1, float z1, float x2, float y2, float z2);
	UNNATURAL_API float uwDistanceEstimate(uint32 a, uint32 b);
	UNNATURAL_API float uwYaw(uint32 position, uint32 towards);

	// entity

	typedef struct UwEntity UwEntity;
	UNNATURAL_API UwEntity *uwEntityPointer(uint32 id);
	UNNATURAL_API uint32 uwEntityId(UwEntity *entity);
	UNNATURAL_API void uwAllEntities(UwIds *data);

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

#endif // unnatural_uwapi_common_h_sdr8g4h1u