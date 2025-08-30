Economy
=======

Recipes And Constructions
-------------------------

Resources are mined from deposits, or processed from other resources.
Producing units and researching upgrades works the same as recipes.

.. tab-set::
   :sync-group: language

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

          # find closest viable position for miner:
          p = uw_world.find_construction_placement(DRILL_CONSTRUCTION_ID, home_position, METAL_RECIPE_ID) # recipe id is optional
          if p == INVALID:
              return

          # place construction:
          uw_commands.place_construction(DRILL_CONSTRUCTION_ID, p, 0, METAL_RECIPE_ID, Priority.High) # yaw, recipe, and priority are optional
          
          # recipe and priority can be changed later:
          uw_commands.set_recipe(own_id, ANOTHER_RECIPE_ID)
          uw_commands.set_priority(own_id, Priority.Normal)

   .. tab-item:: C#
      :sync: csharp

      .. code-block:: csharp

          // find closest viable position for miner:
          uint p = World.FindConstructionPlacement(DRILL_CONSTRUCTION_ID, homePosition, METAL_RECIPE_ID); // recipe id is optional
          if (p == Entity.Invalid):
              return;

          // place construction:
          Commands.PlaceConstruction(DRILL_CONSTRUCTION_ID, p, 0, METAL_RECIPE_ID, UwPriorityEnum.High); // yaw, recipe, and priority are optional
          
          // recipe and priority can be changed later:
          Commands.SetRecipe(ownId, ANOTHER_RECIPE_ID)
          Commands.SetPriority(ownId, UwPriorityEnum.Normal)

   .. tab-item:: C++
      :sync: cpp

      .. code-block:: cpp

          // todo

Logistics
---------

Resources are automatically transported by trucks.
They will fulfill tasks by their priority, and on first-come-first-serve basis.

.. tab-set::
   :sync-group: language

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

          # percentage of trucks that are idle:
          100.0 * uw_world.my_force_statistics().logisticsUnitsIdle / uw_world.my_force_statistics().logisticsUnitsTotal

   .. tab-item:: C#
      :sync: csharp

      .. code-block:: csharp

          // percentage of trucks that are idle:
          100.0 * World.MyForceStatistics().logisticsUnitsIdle / World.MyForceStatistics().logisticsUnitsTotal

Expansion Bases
---------------

Each map contains predefined set of starting positions.
These can have some additional conditions to be used as starting base, eg. actual number of forces in the game.
Anyway, these positions can be used to easily find suitable expansion bases.

.. tab-set::
   :sync-group: language

   .. tab-item:: Python
      :sync: python

      .. code-block:: python

          # potential expansion bases:
          list({p.position for p in uw_map.starting_positions()}) # make the positions unique

   .. tab-item:: C#
      :sync: csharp

      .. code-block:: csharp

          // potential expansion bases:
          Map.StartingPositions().Select(p => p.position).Distinct().ToList();

   .. tab-item:: C++
      :sync: cpp

      .. code-block:: cpp

          // todo
