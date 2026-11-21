Upgrade
-------
Upgrades improve combat or economy of specified units/buildings of the same player.
The upgrade itself defines the improvements that it will apply, and units have a list of upgrades that may be applied to them.

The upgrades are temporary, and will disappear after specified duration.
Multiple same upgrades stack together, up to a specified limit.

Example
=======

.. code-block:: ini

	[texts]
	title = /example/upgrades/damage/title
	description = /example/upgrades/damage/description

	[upgrade]
	duration = 90 # seconds
	limit = 15

	[values]
	damage = 20 # 20 % for each item, tops at 300 % at the limit of 15 items
	attackRange = 0
	splashRadius = 0
	defense = 0
	regenDelay = 0
	regenSpeed = 0
	movementSpeed = 0
	processingSpeed = 0
	visionRange = 0
	stealthRange = 0

	[graphics]
	icon = /example/upgrades/damage/icon.png

	[tags]
	military
	weapons
