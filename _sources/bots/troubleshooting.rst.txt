Troubleshooting
===============

.. warning::
	Do *not* use Flatpak for Steam on Linux.

.. dropdown:: Unable to load DLL 'unnatural-uwapi-hard'

	Make sure you have installed Unnatural Worlds in Steam.

	If your Steam games are in non-default location, define the environment variable ``UNNATURAL_ROOT`` to the directory containing the library.  
	Example: ``C:\Program Files (x86)\Steam\steamapps\common\Unnatural Worlds\bin``

.. dropdown:: OSError: cannot load library 'unnatural-uwapi-hard'

	Make sure you have installed Unnatural Worlds in Steam.

	If your Steam games are in non-default location, define the environment variable ``UNNATURAL_ROOT`` to the directory containing the library.  
	Example: ``C:\Program Files (x86)\Steam\steamapps\common\Unnatural Worlds\bin``

.. dropdown:: Failed to initialize Steam API

	Make sure that Steam is running and logged in.  
	It must run under the same user as the program.

.. dropdown:: Linux laptop with switchable GPUs

	To run using nvidia gpu:

	.. code-block:: bash

		__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia your_program
