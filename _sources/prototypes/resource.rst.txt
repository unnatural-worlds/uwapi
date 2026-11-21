Resource
--------
Defines properties of a resource - aka a crate/pallet/barrel that would exist in the world.

Example
=======

.. code-block:: ini

	[texts]
	title = /example/resources/iron/title
	description = /example/resources/iron/description

	[resource]
	global = false
	tutorialRequiresNoProduction = false
	maximumProcessingOutput = 10
	verticalSeparationDistance = 3.5 # meters

	[graphics]
	icon = /example/resources/iron/icon.png
	base = /example/resources/iron/iron.glb

	[sounds]
	selection = /example/resources/iron/selection.wav
	manipulation = /example/resources/iron/manipulation.wav

	[tags]
	material
	mineable
