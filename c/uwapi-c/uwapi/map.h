#ifndef unnatural_uwapi_map_h_mne1bef54
#define unnatural_uwapi_map_h_mne1bef54

#include "core.h"

#ifdef __cplusplus
extern "C"
{
#endif

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

	// miscellaneous

	UNNATURAL_API void uwAreaRange(float x, float y, float z, float radius, UwIds *data);
	UNNATURAL_API void uwAreaConnected(uint32 position, float radius, UwIds *data);
	UNNATURAL_API void uwAreaNeighborhood(uint32 position, float radius, UwIds *data);
	UNNATURAL_API void uwAreaExtended(uint32 position, float radius, UwIds *data);

	UNNATURAL_API bool uwTestVisible(float x1, float y1, float z1, float x2, float y2, float z2);
	UNNATURAL_API bool uwTestShooting(uint32 shooterPosition, uint32 shooterProto, uint32 targetPosition, uint32 targetProto);
	UNNATURAL_API float uwDistanceLine(float x1, float y1, float z1, float x2, float y2, float z2);
	UNNATURAL_API float uwDistanceEstimate(uint32 a, uint32 b);
	UNNATURAL_API float uwYaw(uint32 position, uint32 towards);
	UNNATURAL_API bool uwTestConstructionPlacement(uint32 constructionPrototype, uint32 position);
	UNNATURAL_API uint32 uwFindConstructionPlacement(uint32 constructionPrototype, uint32 position);

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_map_h_mne1bef54
