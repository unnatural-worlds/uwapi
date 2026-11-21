Mods
====
Guide on making mods for Unnatural Worlds.

.. warning::
	Making mods is not yet fully supported.

A mod is a collection of assets that can modify the look and/or behavior of any map.
It may contain :ref:`prototypes <prototypes/index:Prototypes>`, :ref:`scripts <code/scripts:Scripts>`, or any other :ref:`assets <assets/index:Assets>`.

Assets found in a mod have precedence over assets in a map or in the base game.
However, when multiple mods contain same asset id, only one of them will load, according to mods order, which may lead to serious issues.
Managing mods with clashing assets ids is left to the player.
