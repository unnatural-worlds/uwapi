#ifndef unnatural_uwapi_common_h_sdr8g4h1u
#define unnatural_uwapi_common_h_sdr8g4h1u

#if defined(UNNATURAL_SCRIPTS) == defined(UNNATURAL_BOTS)
	#error Exactly one of UNNATURAL_SCRIPTS or UNNATURAL_BOTS must be defined
#endif

#ifndef UNNATURAL_API
	#define UNNATURAL_API
#endif // !UNNATURAL_API

#ifndef UNNATURAL_ENTRY
	#define UNNATURAL_ENTRY
#endif

#ifndef UNNATURAL_POINTER
	#define UNNATURAL_POINTER(X) X
#endif // !UNNATURAL_POINTER

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

	typedef uint8_t uint8;
	typedef int8_t sint8;
	typedef uint16_t uint16;
	typedef int16_t sint16;
	typedef uint32_t uint32;
	typedef int32_t sint32;
	typedef uint64_t uint64;
	typedef int64_t sint64;

	static const uint32 UW_VERSION = 24;
	static const uint32 UW_GameTicksPerSecond = 20;

	typedef struct UwIds
	{
		UNNATURAL_POINTER(const uint32 *) ids;
		uint32 count;
	} UwIds;

	typedef enum UwPriorityEnum
	{
		UwPriorityEnum_Disabled = 0,
		UwPriorityEnum_Normal = 1,
		UwPriorityEnum_High = 2,
	} UwPriorityEnum;

	typedef enum UwForeignPolicyEnum
	{
		UwForeignPolicyEnum_None = 0,
		UwForeignPolicyEnum_Self = 1,
		UwForeignPolicyEnum_Ally = 2,
		UwForeignPolicyEnum_Neutral = 3,
		UwForeignPolicyEnum_Enemy = 4,
	} UwForeignPolicyEnum;

	typedef enum UwChatTargetFlags
	{
		UwChatTargetFlags_None = 0,
		UwChatTargetFlags_Server = 1 << 0,
		UwChatTargetFlags_Direct = 1 << 1,
		UwChatTargetFlags_Self = 1 << 2,
		UwChatTargetFlags_Allies = 1 << 3,
		UwChatTargetFlags_Neutral = 1 << 4,
		UwChatTargetFlags_Enemy = 1 << 5,
		UwChatTargetFlags_Observer = 1 << 6,
		UwChatTargetFlags_Admin = 1 << 7,
		UwChatTargetFlags_Players = UwChatTargetFlags_Self | UwChatTargetFlags_Allies | UwChatTargetFlags_Neutral | UwChatTargetFlags_Enemy,
		UwChatTargetFlags_Everyone = UwChatTargetFlags_Players | UwChatTargetFlags_Observer | UwChatTargetFlags_Admin,
	} UwChatTargetFlags;

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_common_h_sdr8g4h1u
