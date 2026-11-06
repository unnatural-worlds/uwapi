Unit
----
Both buildings and units are treated as units in the game.

.. note::
	Some neutral objects, such as trees, rocks, ore deposits, etc. are units too.

The prototype contains combat related properties, movement speeds or building radius, a list of available recipes, and a list of applicable upgrades.
Additionally, there are several boolean properties, which modify behavior or requirements of the unit/building.

Example unit
============

.. code-block:: ini

	[texts]
	title = /example/units/tank/title
	description = /example/units/tank/description

	[unit]
	mobile = true
	visionRange = 110 # meters
	stealthRange = 60 # meters
	aggroRange = 90 # meters
	minimapIconScale = 1
	score = 15
	deathDuration = 10 # seconds

	[defense]
	theme = mechanical
	life = 180
	lifeRegen = 0
	regenDelay = 15 # seconds
	initialLife = 180

	[speeds]
	road = 20 # meters per second
	flat = 20
	rough = 15
	cliffs = 0
	water = 0

	[weapon]
	rate = 2.0 # shots per second
	dps = 18
	damageFractionAtLowLife = 0.5
	minRange = 0 # meters
	range = 35 # meters
	elevation = 0 # degrees
	targetElevation = 0 # degrees
	splashRadius = 0 # meters
	splashFractionAtEdge = 0.7
	splashFractionToFriendly = 0
	theme = kinetic

	[graphics]
	icon = /example/units/tank/icon.png
	base = /example/units/tank/tank.glb?base
	turret = /example/units/tank/tank.glb?turret
	cannon = /example/units/tank/tank.glb?cannon
	death = /example/units/tank/tank_death.glb
	wreck = /example/units/tank/tank_wreck.glb
	footprints = /example/units/tank/footprints.glb
	symbol = /example/symbols/front_line.png

	[animations]
	attack = /example/units/tank/tank.glb?attack
	death = /example/units/tank/tank_death.glb?death
	idle = /example/units/tank/tank.glb?idle
	random = /example/units/tank/tank.glb?random
	walk = /example/units/tank/tank.glb?walk

	[sounds]
	attack = /example/units/tank/attack.wav
	death = /example/units/tank/death.wav
	hit = /example/units/tank/hit.wav
	impact = /example/units/tank/impact.wav
	selection = /example/units/tank/selection.wav
	walk = /example/units/tank/walk.wav
	random = /example/units/tank/random.wav
	spawn = /example/units/tank/spawn.wav

	[randomAnimation]
	delayMin = 20 # seconds
	delayMax = 90
	duration = 1

	[particles]
	attack = 12030
	death = 12030
	hit = 11030
	impact = 12030
	splash = 12030

	[pivots]
	weakPoint = 0 1 0
	cargo = 0 1 0
	weakRadius = 1
	iconsAltitude = 1
	turret = 0 1 0
	cannon = 0 1.5 0
	muzzle = 0 1.5 -1.2

	[restrictedModeRequirements]
	skipImplicit = false

	[tags]
	vehicle
	military

Example building
================

.. code-block:: ini

	[texts]
	title = /example/buildings/farm/title
	description = /example/buildings/farm/description

	[unit]
	mobile = false
	visionRange = 70 # meters
	minimapIconScale = 1
	score = 25
	deathDuration = 15 # seconds
	radius = 15 # meters

	[defense]
	theme = building
	life = 500
	lifeRegen = 0 # life per second
	regenDelay = 30 # seconds
	initialLife = 500

	[terrains]
	# each line is one condition and all conditions have to be met
	# format: list of terrain indices = minimum and maximum percentage coverage
	road,flat = 100, 100 # roads + flat must cover 100 % of tiles

	[graphics]
	icon = /example/buildings/farm/icon.png
	construction = /example/buildings/farm/farm_construction.glb
	base = /example/buildings/farm/farm.glb
	death = /example/buildings/farm/farm_death.glb
	symbol = /example/symbols/economy.png

	[animations]
	construction = /example/buildings/farm/farm_construction.glb?construction
	idle = /example/buildings/farm/farm.glb?idle
	processing = /example/buildings/farm/farm.glb?processing
	death = /example/buildings/farm/farm_death.glb?death

	[sounds]
	construction = /example/buildings/farm/construction.wav
	death = /example/buildings/farm/death.wav
	hit = /example/buildings/farm/hit.wav
	processing = /example/buildings/farm/processing.wav
	selection = /example/buildings/farm/selection.wav
	spawn = /example/buildings/farm/spawn.wav

	[particles]
	hit = 11030
	death = 12030

	[pivots]
	weakPoint = 0 2 0
	processingParticles = 0 1 0
	processingHologram = 0 2 0
	weakRadius = 5
	iconsAltitude = 2

	[recipes]
	/example/recipes/food.proto

	[upgrades]
	/example/upgrades/fortification.proto

	[restrictedModeRequirements]
	skipImplicit = false

	[tags]
	building
	economy
