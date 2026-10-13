Tags
----
All prototypes may have associated some tags with them.
Tags are short strings (mapped to unique ids), that are provided by the game/map/mods to help programs understand the nuances of that particular prototype.
Tags are *not* used by the game, except by the built-in AI/bot, which uses tags to alter behavior of some units.
Tags may be used by both Bots and Scripts.

- ``amphibious`` - moves on water and land, but not cliffs.
- ``ballistic`` - attacks in an arc.
- ``building`` - a building, duh.
- ``cliff_walking`` - moves on land and cliffs.
- ``decoration`` - just a decoration.
- ``deposit`` - contains ore; build a miner over this unit to gather resources.
- ``detector`` - detects stealthy units in its vision.
- ``fire_support`` - unit class.
- ``flanking`` - unit class.
- ``flying`` - can move on all of water, land, and cliffs.
- ``front_line`` - unit class.
- ``home`` - the center of your base. dont let it die.
- ``miner`` - generates resources, usually from ore deposits.
- ``navy`` - moves on water only.
- ``non_combat`` - not intended for combat, even if it has an attack/explosion.
- ``non_progression`` - an alternative for another prototype (this tag is used to break cyclic dependencies).
- ``production`` - produces more units.
- ``regen`` - has life regeneration.
- ``research`` - produces upgrades.
- ``scout`` - unit class.
- ``siege`` - unit class.
- ``splash`` - area-of-effect attack/explosion.
- ``stealth`` - cannot be seen by enemy, unless in close proximity or in range of a detector.
- ``suicidal`` - sacrifices itself when attacking.
- ``t1`` - first level of technology.
- ``t2`` - second level of technology.
- ``t3`` - third level of technology.
- ``tower`` - stationary defensive structure.
- ``unarmed`` - unit class.
- ``wall`` - stationary path blocking structure.
- ``worker`` - carries resources, automatic control by logistics planning.
