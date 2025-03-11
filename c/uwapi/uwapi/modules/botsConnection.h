#ifndef unnatural_uwapi_botsConnection_h_d5fgh4df5dfgh
#define unnatural_uwapi_botsConnection_h_d5fgh4df5dfgh

#include "common.h"

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef UNNATURAL_BOTS

	UNNATURAL_API void uwInitialize(uint32 version);
	UNNATURAL_API void uwDeinitialize(void);

	typedef void (*UwExceptionCallbackType)(const char *message);
	UNNATURAL_API void uwSetExceptionCallback(UwExceptionCallbackType callback);

	typedef enum UwSeverityEnum
	{
		UwSeverityEnum_Note = 0,
		UwSeverityEnum_Hint = 1,
		UwSeverityEnum_Warning = 2,
		UwSeverityEnum_Info = 3,
		UwSeverityEnum_Error = 4,
		UwSeverityEnum_Critical = 5,
	} UwSeverityEnum;
	typedef struct UwLogCallback
	{
		const char *message;
		const char *component;
		UwSeverityEnum severity;
	} UwLogCallback;
	typedef void (*UwLogCallbackType)(const UwLogCallback *data);
	UNNATURAL_API void uwSetLogCallback(UwLogCallbackType callback);
	UNNATURAL_API void uwInitializeConsoleLogger(void);
	UNNATURAL_API void uwLog(UwSeverityEnum severity, const char *message);

	typedef enum UwConnectionStateEnum
	{
		UwConnectionStateEnum_None = 0,
		UwConnectionStateEnum_Connecting = 1,
		UwConnectionStateEnum_Connected = 2,
		UwConnectionStateEnum_Error = 3,
	} UwConnectionStateEnum;
	typedef void (*UwConnectionStateCallbackType)(UwConnectionStateEnum state);
	UNNATURAL_API void uwSetConnectionStateCallback(UwConnectionStateCallbackType callback);
	UNNATURAL_API UwConnectionStateEnum uwConnectionState(void);

	UNNATURAL_API void uwSetConnectStartGui(bool enabled, const char *extraCmdParams);
	UNNATURAL_API void uwSetConnectAsObserver(bool observer);
	UNNATURAL_API bool uwConnectFindLan(uint64 timeoutMicroseconds);
	UNNATURAL_API void uwConnectDirect(const char *address, uint16 port);
	UNNATURAL_API void uwConnectLobbyId(uint64 lobbyId);
	UNNATURAL_API bool uwConnectEnvironment();
	UNNATURAL_API void uwConnectNewServer(uint32 visibility, const char *name, const char *extraCmdParams);
	UNNATURAL_API bool uwTryReconnect(void);
	UNNATURAL_API void uwDisconnect(void);

	typedef struct UwPerformanceStatistics
	{
		float gameSpeed;
		float mainThreadUtilization;
		float ping; // ms
		uint32 networkUp; // kb/s
		uint32 networkDown; // kb/s
	} UwPerformanceStatistics;
	UNNATURAL_API void uwPerformanceStatistics(UwPerformanceStatistics *data);

#endif

#ifdef __cplusplus
} // extern C
#endif

#endif // unnatural_uwapi_botsConnection_h_d5fgh4df5dfgh
