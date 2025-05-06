Setup
=====
You can write your bot in any language, as long as it can load a dynamic/shared library (.dll/.so).
The shared library is distributed together with the game.

The uwapi repository contains c/c++ headers for all functions and structures provided by the library.
Furthermore, it contains convenient wrappers for Python and C# for easy start.

.. important::
	Copy ``steam_appid.txt`` into the ``bin`` folder.

The file ``steam_appid.txt`` tells Steam that this is developer copy of the game.
It allows running multiple processes of the game simultaneously, and to start the programs directly from outside the Steam.
This allows you to retain full control over your bot program - it makes it possible to develop and debug it from inside your IDE.
You may also start the game client, game server, built-in AI, or any other associated programs from your terminal.
You will find the ``steam_appid.txt`` in the uwapi repository.
Copy it into the ``bin`` folder, next to the game executable.

.. important::
	If you installed Unnatural World in non-default location, define environment variable ``UNNATURAL_ROOT`` to the directory containing the library.

.. tab-set::

   .. tab-item:: Windows
      :sync: windows

      Default path: ``C:\Program Files (x86)\Steam\steamapps\common\Unnatural Worlds\bin``

   .. tab-item:: Linux
      :sync: linux

      Default path: ``~/.steam/steam/steamapps/common/Unnatural Worlds/bin``
