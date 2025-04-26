Bots
====
Guide on writing custom AI/bots for Unnatural Worlds.

You can write your bot in any language, as long as it can load a dynamic/shared library (.dll/.so).
The shared library is distributed together with the game.
The uwapi repository contains c/c++ headers for all functions and structures provided by the library.

The uwapi repository also contains convenient wrappers for Python and for C# for quicker start of writing your bot.

The bots api is designed such that you retain full control over your bot program - aka it makes it possible to develop and debug it the way you are used to.
However, to be able to start the game outside of the Steam, it is necessary to copy the file ``steam_appid.txt`` (contained in the uwapi repository) into the ``bin`` folder, next to the game executable.
This also allows you to start the game, and all other accompanying programs, from command line or from bash, which allows you to manually start the server, and connect any number of bots and human players.

.. toctree::
	troubleshooting
