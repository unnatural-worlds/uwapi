#ifndef unnatural_uwapi_scriptsServer_h_w4e5rhbsds
#define unnatural_uwapi_scriptsServer_h_w4e5rhbsds

#include "common.h"

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef UNNATURAL_SCRIPTS

	UNNATURAL_API uint32 uwCreateEntity(uint32 proto, uint32 position, uint32 owner);
	UNNATURAL_API void uwDestroyEntity(uint32 entity);

	UNNATURAL_API uint32 uwChangeOwner(uint32 entity, uint32 owner);

	UNNATURAL_API void uwSetPositionYaw(uint32 entity, uint32 position, float yaw);
	UNNATURAL_API void uwSetPosition(uint32 entity, uint32 position);
	UNNATURAL_API void uwSetYaw(uint32 entity, float yaw);
	UNNATURAL_API void uwMove(uint32 entity, uint32 position); // neighbor only
	UNNATURAL_API void uwMoveYaw(uint32 entity, uint32 position, float yaw);
	UNNATURAL_API void uwMoveTo(uint32 entity, uint32 position);

	UNNATURAL_API void uwSetLife(uint32 entity, uint32 life);
	UNNATURAL_API void uwSetAim(uint32 entity, uint32 target); // target = 0 to remove
	UNNATURAL_API void uwSetRecipe(uint32 entity, uint32 recipe); // recipe = 0 to remove
	UNNATURAL_API void uwSetPriority(uint32 entity, UwPriorityEnum priority);
	UNNATURAL_API void uwSetCooldown(uint32 entity, uint32 ticks);

	UNNATURAL_API void uwSetAmount(uint32 entity, uint32 amount);
	UNNATURAL_API void uwSetAttached(uint32 entity, uint32 target); // target = 0 to detach

	UNNATURAL_API uint32 uwCreateForce(void);
	UNNATURAL_API void uwDestroyForce(uint32 force);
	UNNATURAL_API void uwSetPlayerForce(uint32 player, uint32 force);
	UNNATURAL_API void uwSetForceColor(uint32 force, float r, float g, float b);
	UNNATURAL_API void uwSetForceFinish(uint32 force, bool winner, bool defeated);
	UNNATURAL_API void uwSetForceStartingTeam(uint32 force, uint32 team);
	UNNATURAL_API void uwSetForceStartingPosition(uint32 force, uint32 position);
	UNNATURAL_API void uwSetForeignPolicy(uint32 force1, uint32 force2, UwForeignPolicyEnum policy);

	UNNATURAL_API void uwStandardVictoryConditions(bool enable);
	UNNATURAL_API void uwSendChat(const char *msg, UwChatTargetFlags flags, uint32 target);

	UNNATURAL_API void uwPrint(const char *msg);
	UNNATURAL_API uint32 uwRand(void);

#endif

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_scriptsServer_h_w4e5rhbsds
