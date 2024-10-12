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

	static const uint32 UW_GameTicksPerSecond = 20;

	typedef struct UwIds
	{
		const uint32 *ids;
		uint32 count;
	} UwIds;

	// prototypes

	typedef enum UwPrototypeTypeEnum
	{
		UwPrototypeTypeEnum_None = 0,
		UwPrototypeTypeEnum_Resource = 1,
		UwPrototypeTypeEnum_Recipe = 2,
		UwPrototypeTypeEnum_Construction = 3,
		UwPrototypeTypeEnum_Unit = 4,
	} UwPrototypeTypeEnum;
	UNNATURAL_API void uwAllPrototypes(UwIds *data);
	UNNATURAL_API UwPrototypeTypeEnum uwPrototypeType(uint32 prototypeId);
	UNNATURAL_API const char *uwPrototypeJson(uint32 prototypeId);
	UNNATURAL_API const char *uwDefinitionsJson(void);

	// map

	typedef struct UwMapInfo
	{
		const char *name;
		const char *guid;
		const char *path;
		uint32 maxPlayers;
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
		uint32 clusterIndex;
		uint8 terrain;
		bool border;
	} UwTile;
	UNNATURAL_API void uwTile(uint32 index, UwTile *data);

	// clusters

	UNNATURAL_API uint32 uwClustersCount(void);
	// todo other data for clusters

	// overview

	typedef enum UwOverviewFlags
	{
		UwOverviewFlags_None = 0,
		UwOverviewFlags_Resource = 1 << 0,
		UwOverviewFlags_Construction = 1 << 1,
		UwOverviewFlags_MobileUnit = 1 << 2,
		UwOverviewFlags_StaticUnit = 1 << 3,
		UwOverviewFlags_Unit = UwOverviewFlags_MobileUnit | UwOverviewFlags_StaticUnit,
	} UwOverviewFlags;
	UNNATURAL_API UwOverviewFlags uwOverviewFlags(uint32 position);
	UNNATURAL_API void uwOverviewIds(uint32 position, UwIds *data);
	typedef struct UwOverviewExtract
	{
		const UwOverviewFlags *flags;
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

	typedef enum UwUnitStateFlags
	{
		UwUnitStateFlags_None = 0,
		UwUnitStateFlags_Shooting = 1 << 0,
		UwUnitStateFlags_Processing = 1 << 1, // processing recipe
		UwUnitStateFlags_Rebuilding = 1 << 2, // changing recipe
	} UwUnitStateFlags;
	typedef struct UwUnitComponent
	{
		UwUnitStateFlags state;
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

	typedef enum UwPriorityEnum
	{
		UwPriorityEnum_Disabled = 0,
		UwPriorityEnum_Normal = 1,
		UwPriorityEnum_High = 2,
	} UwPriorityEnum;
	typedef struct UwPriorityComponent
	{
		UwPriorityEnum priority;
	} UwPriorityComponent;
	UNNATURAL_API bool uwFetchPriorityComponent(UwEntity *entity, UwPriorityComponent *data);

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
	UNNATURAL_API bool uwFetchPlayerComponent(UwEntity *entity, UwPlayerComponent *data);

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
		uint32 team;
		UwForceStateFlags state;
	} UwForceComponent;
	UNNATURAL_API bool uwFetchForceComponent(UwEntity *entity, UwForceComponent *data);

	typedef struct UwForceDetailsComponent
	{
		uint64 killValue;
		uint64 lossValue;
		uint32 startingPosition;
	} UwForceDetailsComponent;
	UNNATURAL_API bool uwFetchForceDetailsComponent(UwEntity *entity, UwForceDetailsComponent *data);

	typedef enum UwForeignPolicyEnum
	{
		UwForeignPolicyEnum_None = 0,
		UwForeignPolicyEnum_Self = 1,
		UwForeignPolicyEnum_Ally = 2,
		UwForeignPolicyEnum_Neutral = 3,
		UwForeignPolicyEnum_Enemy = 4,
	} UwForeignPolicyEnum;
	typedef struct UwForeignPolicyComponent
	{
		uint32 forces[2];
		UwForeignPolicyEnum policy;
	} UwForeignPolicyComponent;
	UNNATURAL_API bool uwFetchForeignPolicyComponent(UwEntity *entity, UwForeignPolicyComponent *data);

	typedef struct UwDiplomacyProposalComponent
	{
		uint32 offeror;
		uint32 offeree;
		UwForeignPolicyEnum proposal;
	} UwDiplomacyProposalComponent;
	UNNATURAL_API bool uwFetchDiplomacyProposalComponent(UwEntity *entity, UwDiplomacyProposalComponent *data);

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_common_h_sdr8g4h1u
