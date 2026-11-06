Recipe
------
Defines a transformation of resources, units, and upgrades.
It contains amounts and ids of inputs and outputs.
Also defines the duration of the recipe.
Recipes are processed in buildings/units.

Some recipes have a *place-over* requirement, which is an id of a unit prototype, that the building must be placed on, in order for the recipe to operate.

Example
=======

.. code-block:: ini

	[texts]
	title = /example/recipes/smelt/title
	description = /example/recipes/smelt/description

	[recipe]
	keybind = S
	keybindMods = 0
	duration = 4 # seconds
	placeOver = /example/ores/ore.proto

	[inputs]
	/example/resources/ore.proto = 2

	[outputs]
	/example/resources/iron.proto = 1

	[graphics]
	icon = /example/resources/iron/icon.png
	hologram = /example/resources/iron/iron.glb;hologram

	[particles]
	color = 1.0 0.45 0.1
	processing = 1001 # id of particle effect
	period = 0.25 # seconds

	[restrictedModeRequirements]
	skipImplicit = false

	[tags]
	industry
	smelting
