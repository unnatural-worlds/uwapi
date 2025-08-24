Combat & Upgrades
=================

Shooting
--------

Requirements for shooting:

- the target is withing shooting range.
- the target is visible in line (or arc).
- the target is not covered by fog-of-war.

.. note::
   Fog-of-war is not yet implemented.

Most units can shoot in straight line only.
Some units can shoot in an arc, which is defined by ``shooterElevation`` and ``targetElevation``.
This allows to shoot "over a horizon", or "behind a corner".

Explosions
----------

A unit may have any combination (or none) of the following triggers:

- ``explodesWhenAttacks`` - suicidal unit.
- ``explodesWhenKilled`` - explodes when the unit is naturally killed.
- ``explodesWhenSelfDestructed`` - explodes when the unit receives self-destruct command from owner.

When a unit explodes, it does splash damage in area around it.
Damage type of the explosion may be different from shooting.

Splash
------

Splash means the damage is an area-of-effect.
It is centered at the target of shooting, or at the unit that explodes, and is circular with specified radius.

Damage of splash decreases with distance from center, which is determined by ``splashFractionAtEdge``.
It may also affect own/ally units, depending on ``splashFractionToFriendly``.

Damage And Armor Types
----------------------

Each unit has associated armor type, and each shooting (or explosion) has associated damage type.
The game has a table that defines a fraction for each combination of damage type with each armor type.
Some values are over 100 % and some are below.

For example, energy shield is designed to be highly resistant to lasers and plasma, which are most often used in long-range guns; and antimatter guns are designed for destroying buildings.

Life Regeneration
-----------------

Life regeneration has a delay, which is extended whenever the unit is attacked, or whenever the unit itself shoots.
When the delay expires, the unit starts healing at the specified rate.

Upgrades
--------

Research usually consumes some resources to produce upgrades.
Upgrades will stack, up to a specified limit.
This means that the upgrades have a ramp-up phase.
When research stops, the upgrades will dissipate after some time.

Most upgrades apply percentage increase to one or more of the properties of a unit.

Each unit has a list of upgrades that apply to it.
