Race
----
Each player selects one race that they play as.
The race defines their starting resources and units, and a list of available constructions.

Note that neither resources, recipes, units, or upgrades are inherently associated with any particular race.
There are no restrictions on units that the player may control, if they get hold of them.

Example
=======

.. code-block:: ini

	[texts]
	title = /example/race/title
	description = /example/race/description

	[race]
	package = /example/race.pack

	[startingProvisions]
	/example/resources/gold.proto = 10
	/example/resources/wood.proto = 5

	[constructions]
	/example/constructions/townhall.proto
	/example/constructions/farm.proto
	/example/constructions/barracks.proto
