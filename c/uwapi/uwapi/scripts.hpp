#ifndef unnatural_uwapi_scripts_hpp_zhgfa8g4
#define unnatural_uwapi_scripts_hpp_zhgfa8g4

#include <vector>

#include "scripts.h"

namespace uw
{
	template<class T>
	auto makeVector(T *data, uint32 cnt)
	{
		std::vector<std::remove_cv_t<T>> res;
		res.resize(cnt);
		memcpy(res.data(), data, cnt * sizeof(T));
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
}

#endif // unnatural_uwapi_scripts_hpp_zhgfa8g4
