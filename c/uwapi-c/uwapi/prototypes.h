#ifndef unnatural_uwapi_prototypes_h_hrs564gj
#define unnatural_uwapi_prototypes_h_hrs564gj

#include "core.h"

#ifdef __cplusplus
extern "C"
{
#endif

	// prototypes

	UNNATURAL_API uint32 uwPrototypesCount(void);
	UNNATURAL_API uint32 uwPrototypeIdFromIndex(uint32 index);
	UNNATURAL_API uint32 uwPrototypeType(uint32 prototypeId);
	UNNATURAL_API const char *uwPrototypeJson(uint32 prototypeId);
	UNNATURAL_API const char *uwDefinitionsJson(void);

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_prototypes_h_hrs564gj
