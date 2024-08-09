# uwapi
Language bindings for writing AI bots for Unnatural Worlds

Language-specific instructions are in the respective folders.

## Troubleshooting

> Unable to load DLL 'unnatural-uwapi-hard'
> OSError: cannot load library 'unnatural-uwapi-hard'

Make sure you have installed Unnatural Worlds in Steam.

If your steam games are in non-default location, define environment variable `UNNATURAL_ROOT` to the directory containing the library.
Eg. `C:\Program Files (x86)\Steam\steamapps\common\Unnatural Worlds\bin`.

> failed to initialize steam api

Make sure that Steam is running and logged in.
It must run under the same user.

On linux: avoid using flatpack for Steam.

> Linux laptop with switchable GPUs

```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia your_program
```
