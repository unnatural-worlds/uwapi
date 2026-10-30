#ifndef unnatural_uwapi_scripts_hpp_zhgfa8g4
#define unnatural_uwapi_scripts_hpp_zhgfa8g4

#include <algorithm>
#include <cmath>
#include <cstring> // memcpy
#include <vector>

#include "scripts.h"

namespace uw
{
	// utilities

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

	// forces and players

	namespace privat
	{
		inline void setForceColorWithShift(uint32 force, uint32 index, uint32 total, float r, float g, float b)
		{
			if (total > 1)
			{
				const float hueShift = 90.0f * (static_cast<float>(index) / (total - 1) - 0.5f);
				const float maxC = std::max({ r, g, b });
				const float minC = std::min({ r, g, b });
				const float delta = maxC - minC;
				float h = 0.0f;
				const float s = (maxC > 0.0f) ? delta / maxC : 0.0f;
				const float v = maxC;
				if (delta > 0.0f)
				{
					if (maxC == r)
						h = 60.0f * std::fmod((g - b) / delta, 6.0f);
					else if (maxC == g)
						h = 60.0f * ((b - r) / delta + 2.0f);
					else
						h = 60.0f * ((r - g) / delta + 4.0f);
					if (h < 0.0f)
						h += 360.0f;
				}
				h = std::fmod(h + hueShift, 360.0f);
				const float c = v * s;
				const float x = c * (1.0f - std::fabs(std::fmod(h / 60.0f, 2.0f) - 1.0f));
				const float m = v - c;
				if (h < 60.0f)
				{
					r = c;
					g = x;
					b = 0.0f;
				}
				else if (h < 120.0f)
				{
					r = x;
					g = c;
					b = 0.0f;
				}
				else if (h < 180.0f)
				{
					r = 0.0f;
					g = c;
					b = x;
				}
				else if (h < 240.0f)
				{
					r = 0.0f;
					g = x;
					b = c;
				}
				else if (h < 300.0f)
				{
					r = x;
					g = 0.0f;
					b = c;
				}
				else
				{
					r = c;
					g = 0.0f;
					b = x;
				}
				r += m;
				g += m;
				b += m;
			}
			uwSetForceColor(force, r, g, b);
		}
	}

	inline void setForceColorPlayer(uint32 force)
	{
		uwSetForceColor(force, 28 / 255.f, 165 / 255.f, 232 / 255.f);
	}

	inline void setForceColorAlly(uint32 force, uint32 index = 0, uint32 total = 1)
	{
		privat::setForceColorWithShift(force, index, total, 0 / 255.f, 186 / 255.f, 0 / 255.f);
	}

	inline void setForceColorEnemy(uint32 force, uint32 index = 0, uint32 total = 1)
	{
		privat::setForceColorWithShift(force, index, total, 253 / 255.f, 137 / 255.f, 14 / 255.f);
	}

	inline void setForceColorNeutral(uint32 force)
	{
		uwSetForceColor(force, 105 / 255.f, 127 / 255.f, 143 / 255.f);
	}

	// world

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

	// map

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

	// prototypes

	inline auto allPrototypes()
	{
		UwIds ids;
		uwAllPrototypes(&ids);
		return makeVector(ids);
	}

	// miscelaneous

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

	// translations

	// this function is used in place of uwHashString
	// the id and english text are scraped by a script to generate templates for translations
	inline uint32 translatedTextHash(const char *id, const char *englishText)
	{
		return uwHashString(id);
		(void)englishText;
	}
}

#endif // unnatural_uwapi_scripts_hpp_zhgfa8g4
