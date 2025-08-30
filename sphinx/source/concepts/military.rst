Military
========

Orders
------

.. note::
   Orders are usable by clients only. Server-side scripts do not have the concept of orders.

You can have multiple orders queued for each unit.

.. tab-set::
   :sync-group: language

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

          # get list of orders of own unit:
          os = uw_commands.orders(own_id)
          
          # order own unit to attack enemy unit (cancels all previous orders):
          uw_commands.order(own_id, uw_commands.fight_to_entity(enemy_id))
          
          # enqueue move order:
          o = uw_commands.run_to_position(tile_index)
          o.priority = o.priority | OrderPriority.Enqueue
          uw_commands.order(own_id, o)

   .. tab-item:: C#
      :sync: csharp

      .. code-block:: csharp

          // get list of orders of own unit:
          var os = Commands.Orders(ownId);
          
          // order own unit to attack enemy unit (cancels all previous orders):
          Commands.Order(ownId, Commands.FightToEntity(enemyId));
          
          // enqueue move order:
          Order o = Commands.RunToPosition(tileIndex);
          o.priority |= UwOrderPriorityFlags.Enqueue;
          Commands.Order(ownId, o);

Tips For Military Maneuvers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tab-set::
   :sync-group: language

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

          # position of enemy military unit that is closest to any of our own units:
          uw_world.my_force_statistics().closestDangerPosition

          # position that is specific distance from target, and closest to us
          surrounding_positions = uw_map.area_neighborhood(target_position, 200)
          specific_distance_position = min(surrounding_positions, key=lambda x: uw_map.distance_estimate(my_position, x))

          # flanking position around target
          surrounding_positions = uw_map.area_neighborhood(target_position, 200)
          surrounding_positions = sorted(surrounding_positions, key=lambda x: uw_map.distance_estimate(my_position, x))
          flanking_position = surrounding_positions[len(surrounding_positions) // 2] # note that this picks left or right flanking position at random

   .. tab-item:: C#
      :sync: csharp

      .. code-block:: csharp

          // position of enemy military unit that is closest to any of our own units:
          World.MyForceStatistics().closestDangerPosition

          // position that is specific distance from target, and closest to us
          var surroundingPositions = Map.AreaNeighborhood(targetPosition, 200);
          var specificDistancePosition = surroundingPositions.OrderBy(x => Map.DistanceEstimate(myPosition, x)).First();

          // flanking position around target
          var surroundingPositions = Map.areaNeighborhood(targetPosition, 200);
          surroundingPositions.Sort((a, b) => Map.DistanceEstimate(myPosition, a).CompareTo(Map.DistanceEstimate(myPosition, b)));
          var flankingPosition = surroundingPositions[surroundingPositions.Count / 2]; // note that this picks left or right flanking position at random

Shooting
--------

Units will automatically target appropriate enemies in their vicinity.

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
When research stops, the upgrades will dissipate over time.

Most upgrades apply percentage increase to one or more of the properties of a unit.

Each unit has a list of upgrades that apply to it.
