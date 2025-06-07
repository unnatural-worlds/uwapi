Map
===
Map is uniquely identified by its GUID.
It will differ even for each version of the same map.

Tiles
-----
The map uses discrete tiles representation (similar to chess), as opposed to continuous space.

Two neighboring tiles are typically 10 meters apart, however, different neighboring pairs will have different distances.

Tiles are indexed `0 .. N-1`.

Data available for each tile:

- Position - 3D coordinates
- Up - 3D vector - direction opposite of *local* gravity
- Neighbors - array of indices of neighboring tiles
- Cluster - index of the cluster this tile belongs to
- Terrain - index of the terrain type at this tile

Clusters
--------
Clusters are aggregations of tiles into smaller connected groups.
It is intended primarily for performance optimizations.
All tiles in one cluster have same terrain.

Clusters are indexed `0 .. M-1`.

Data available for each cluster:

- Neighbors - array of indices of neighboring clusters
- Tile - index of the center-most tile in this cluster

Overview
--------
Automatically updated ids of entities present on each tile.
This is used for performance optimization.

Entities with larger radius will be present in all tiles that they cover, not just the center.

Additionally, bit-flags are available for each tile, with different bits denoting different types of entities present on the tile.

Area Queries
------------
There are multiple functions for finding tiles within some distance.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. card::
         :img-bottom: /_static/area-query-range.svg
         :text-align: center

         **AreaRange**

   .. grid-item::

      .. card::
         :img-bottom: /_static/area-query-connected.svg
         :text-align: center

         **AreaConnected**

   .. grid-item::

      .. card::
         :img-bottom: /_static/area-query-neighborhood.svg
         :text-align: center

         **AreaNeighborhood**

   .. grid-item::

      .. card::
         :img-bottom: /_static/area-query-extended.svg
         :text-align: center

         **AreaExtended**
