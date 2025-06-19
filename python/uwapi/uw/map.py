import math
from typing import List, Optional
from dataclasses import dataclass

from .interop import UwApi, MapStateEnum, OverviewFlagsEnum


@dataclass
class Vector3:
    """Represents a 3D vector with x, y, and z components."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class Map:
    """Provides access to map data and spatial operations."""
    
    def __init__(self, game):
        """Initialize the map interface.
        
        Args:
            game: The game instance
        """
        self._game = game
        
        # Register callbacks
        self._game.add_map_state_callback(self._map_state_changed)
        self._game.add_update_callback(self._updating)
        
        # Map state
        self._name: str = ""
        self._guid: str = ""
        self._path: str = ""
        self._max_players: int = 0
        self._positions: List[Vector3] = []
        self._ups: List[Vector3] = []
        self._neighbors: List[List[int]] = []
        self._terrains: List[bytes] = []
        self._overview: List[OverviewFlagsEnum] = []
    
    # Map property getters
    
    def name(self) -> str:
        """Get the map name."""
        return self._name
        
    def guid(self) -> str:
        """Get the map GUID."""
        return self._guid
        
    def path(self) -> str:
        """Get the map file path."""
        return self._path
        
    def max_players(self) -> int:
        """Get the maximum number of players supported by the map."""
        return self._max_players
        
    def positions(self) -> List[Vector3]:
        """Get all tile positions on the map."""
        return self._positions
        
    def ups(self) -> List[Vector3]:
        """Get all tile up vectors on the map."""
        return self._ups
        
    def neighbors(self) -> List[List[int]]:
        """Get all tile neighbor relationships."""
        return self._neighbors
        
    def neighbors_of_position(self, pos: int) -> List[int]:
        """Get the neighbors of a specific position."""
        if 0 <= pos < len(self._neighbors):
            return self._neighbors[pos]
        return []
        
    def terrains(self) -> List[bytes]:
        """Get terrain data for all tiles."""
        return self._terrains
        
    def overview(self) -> List[OverviewFlagsEnum]:
        """Get overview flags for all tiles."""
        return self._overview
    
    # Map query methods
    
    def entities(self, position: int) -> List[int]:
        """Get all entities at a specific position."""
        return UwApi.overview_ids(position)
        
    def area_range(self, point: Vector3, radius: float) -> List[int]:
        """Get all tiles within a radius of a point."""
        return UwApi.area_range(point.x, point.y, point.z, radius)
        
    def area_connected(self, position: int, radius: float) -> List[int]:
        """Get all tiles connected to a position within a radius."""
        return UwApi.area_connected(position, radius)
        
    def area_neighborhood(self, position: int, radius: float) -> List[int]:
        """Get all tiles in the neighborhood of a position within a radius."""
        return UwApi.area_neighborhood(position, radius)
        
    def area_extended(self, position: int, radius: float) -> List[int]:
        """Get all tiles in the extended area of a position within a radius."""
        return UwApi.area_extended(position, radius)
        
    def test_visible(self, a: Vector3, b: Vector3) -> bool:
        """Test if point b is visible from point a."""
        return UwApi.test_visible(a.x, a.y, a.z, b.x, b.y, b.z)
        
    def test_shooting(
        self,
        shooter_position: int,
        shooter_proto: int,
        shooting_range_upgrade: float,
        target_position: int,
        target_proto: int,
    ) -> bool:
        """Test if a shooter can shoot a target."""
        return UwApi.test_shooting(
            shooter_position, shooter_proto, shooting_range_upgrade, 
            target_position, target_proto
        )
        
    def distance_line(self, ai: int, bi: int) -> float:
        """Calculate the distance between two positions."""
        if (0 <= ai < len(self._positions) and 0 <= bi < len(self._positions)):
            a: Vector3 = self._positions[ai]
            b: Vector3 = self._positions[bi]
            dx: float = a.x - b.x
            dy: float = a.y - b.y
            dz: float = a.z - b.z
            return math.sqrt(dx*dx + dy*dy + dz*dz)
        return float('inf')
        
    def distance_estimate(self, a: int, b: int) -> float:
        """Estimate the distance between two positions (may consider path distance)."""
        return UwApi.distance_estimate(a, b)
        
    def yaw(self, a: int, b: int) -> float:
        """Calculate the yaw (horizontal angle) from position a to position b."""
        return UwApi.yaw(a, b)
        
    def test_construction_placement(
        self, construction_prototype: int, position: int, recipe_proto: int = 0
    ) -> bool:
        """Test if a construction can be placed at a position."""
        return UwApi.test_construction_placement(construction_prototype, position, recipe_proto)
        
    def find_construction_placement(
        self, construction_prototype: int, position: int, recipe_proto: int = 0
    ) -> int:
        """Find a suitable position near the given position for a construction."""
        return UwApi.find_construction_placement(construction_prototype, position, recipe_proto)
    
    # Internal methods
    
    def _load(self):
        """Load map data when the map is ready."""
        self._game.log_info("Loading map data...")
        self._positions = []
        self._ups = []
        self._neighbors = []
        self._terrains = []
        self._overview = []
        
        # Load map info
        map_info = UwApi.map_info()
        if map_info:
            self._name = map_info.name
            self._guid = map_info.guid
            self._path = map_info.path
            self._max_players = map_info.maxPlayers
        
        # Load tiles
        count = UwApi.tiles_count()
        for i in range(count):
            tile = UwApi.tile(i)
            if tile:
                # Extract position
                pos = Vector3(
                    tile.position[0], 
                    tile.position[1], 
                    tile.position[2]
                )
                self._positions.append(pos)
                
                # Extract up vector
                up = Vector3(
                    tile.up[0],
                    tile.up[1],
                    tile.up[2]
                )
                self._ups.append(up)
                
                # Extract neighbors
                neighbors = []
                if hasattr(tile, 'neighborsIndices') and hasattr(tile, 'neighborsCount'):
                    for j in range(tile.neighborsCount):
                        if j < len(tile.neighborsIndices):
                            neighbors.append(tile.neighborsIndices[j])
                self._neighbors.append(neighbors)
                
                # Extract terrain
                self._terrains.append(tile.terrain if hasattr(tile, 'terrain') else 0)
        
        self._game.log_info(f"Map loaded: {self._name} with {count} tiles")
        
    def _map_state_changed(self, map_state: MapStateEnum):
        """Handle map state changes."""
        if map_state == MapStateEnum.Loaded:
            self._load()
            
    def _updating(self, stepping: bool):
        """Handle game updates."""
        if stepping:
            # Update overview flags
            overview_extract = UwApi.overview_extract()
            if overview_extract and hasattr(overview_extract, 'flags') and overview_extract.count > 0:
                self._overview = [OverviewFlagsEnum(f) for f in overview_extract.flags]
            else:
                self._overview = []
        else:
            self._overview = []
