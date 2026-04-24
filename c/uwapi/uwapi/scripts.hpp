#ifndef unnatural_uwapi_scripts_hpp_zhgfa8g4
#define unnatural_uwapi_scripts_hpp_zhgfa8g4

#include <cstring> // memcpy
#include <vector>

#include "scripts.h"

namespace uw
{
	inline float degToRad(float degs)
	{
		return degs * 3.14159 / 180;
	}

	template<class T>
	auto makeVector(T *data, uint32 cnt)
	{
		std::vector<std::remove_cv_t<T>> res;
		res.resize(cnt);
		std::memcpy(res.data(), data, cnt * sizeof(T));
		return res;
	}

	template<class S>
	requires(requires { S::data; })
	auto makeVector(const S *src)
	{
		return makeVector(src->data, src->count);
	}

	inline auto makeVector(const UwIds &ids)
	{
		return makeVector(ids.ids, ids.count);
	}

	inline auto allEntities()
	{
		UwIds ids;
		uwAllEntities(&ids);
		return makeVector(ids);
	}

	inline uint32 entityPosition(uint32 id)
	{
		UwPositionComponent pc;
		if (uwFetchPositionComponent(id, &pc))
			return pc.position;
		return -1;
	}

	inline auto mapMarkers(const char *marker)
	{
		UwMapMarkersArray arr;
		uwMapMarkers(marker, &arr);
		return makeVector(&arr);
	}

	inline UwMapMarker mapMarker(const char *marker)
	{
		UwMapMarkersArray arr;
		uwMapMarkers(marker, &arr);
		if (arr.count != 1)
		{
			uwPrint(marker);
			uwError("mapMarker expects exactly one marker");
		}
		return arr.data[0];
	}

	inline auto shootingControlData(uint32 id)
	{
		struct ShootingControlData
		{
			UwShootingEventEnum type;
			uint16 count;
		};

		uint16_t low = static_cast<uint16_t>(id & 0xFFFF);
		uint16_t high = static_cast<uint16_t>(id >> 16);
		return ShootingControlData{ (UwShootingEventEnum)low, high };
	}
}

#endif // unnatural_uwapi_scripts_hpp_zhgfa8g4
