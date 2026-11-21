Construction
------------
Constructions are similar to recipes, but are manually placed into the world by the player.
It contains amounts of input resources, and has exactly one output unit/building.

Example
=======

.. code-block:: ini

	[texts]
	title = /example/buildings/farm/title
	description = /example/buildings/farm/description

	[construction]
	category = economy
	keybind = F
	keybindMods = 0
	output = /example/buildings/farm.proto
	duration = 45 # seconds
	linePlacement = false

	[inputs]
	/example/resources/wood.proto = 8
	/example/resources/stone.proto = 3

	[graphics]
	icon = /example/buildings/farm/icon.png
	blueprint = /example/buildings/farm/farm.glb;blueprint

	[restrictedModeRequirements]
	skipImplicit = false

	[tags]
	building
	economy
