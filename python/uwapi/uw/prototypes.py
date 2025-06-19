import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from .interop import UwApi, MapStateEnum, PrototypeTypeEnum


@dataclass
class ProtoGeneric:
    """Represents a generic prototype with type, name, and JSON data."""
    type: PrototypeTypeEnum
    name: str
    json: Any


class Prototypes:
    """Provides access to game prototype definitions."""
    
    def __init__(self, game):
        """Initialize the prototypes interface.
        
        Args:
            game: The game instance
        """
        self._game = game
        self._game.add_map_state_callback(self._map_state_changed)
        
        # Initialize prototype data
        self._hit_chances_table: Dict[str, Any] = {}
        self._terrain_types_table: Dict[str, Any] = {}
        
        self._all: List[int] = []
        self._types: Dict[int, ProtoGeneric] = {}
        self._resources: Dict[int, Any] = {}
        self._recipes: Dict[int, Any] = {}
        self._constructions: Dict[int, Any] = {}
        self._units: Dict[int, Any] = {}
    
    # Accessor methods
    
    def all(self) -> List[int]:
        """Get all prototype IDs."""
        return self._all
        
    def type(self, _id: int) -> PrototypeTypeEnum:
        """Get the type of a prototype."""
        return self._types[_id].type if _id in self._types else PrototypeTypeEnum.None_
        
    def name(self, _id: int) -> str:
        """Get the name of a prototype."""
        return self._types[_id].name if _id in self._types else ""
        
    def json(self, _id: int) -> Any:
        """Get the JSON data of a prototype."""
        return self._types[_id].json if _id in self._types else ""
        
    def resource(self, _id: int) -> Optional[Dict]:
        """Get a resource prototype by ID."""
        return self._resources.get(_id)
        
    def recipes(self, _id: int) -> Optional[Dict]:
        """Get a recipe prototype by ID."""
        return self._recipes.get(_id)
        
    def construction(self, _id: int) -> Optional[Dict]:
        """Get a construction prototype by ID."""
        return self._constructions.get(_id)
        
    def unit(self, _id: int) -> Optional[Dict]:
        """Get a unit prototype by ID."""
        return self._units.get(_id)
        
    def hit_chances_table(self) -> Dict[str, Any]:
        """Get the hit chances table."""
        return self._hit_chances_table
        
    def terrain_types_table(self) -> Dict[str, Any]:
        """Get the terrain types table."""
        return self._terrain_types_table
    
    # Internal methods
    
    def _all_ids(self) -> List[int]:
        """Get all prototype IDs from the API."""
        return UwApi.all_prototypes()
        
    def _load_prototypes(self):
        """Load all prototype data."""
        self._game.log_info("Loading prototypes...")
        
        # Reset prototype data
        self._all = []
        self._types = {}
        self._resources = {}
        self._recipes = {}
        self._constructions = {}
        self._units = {}
        
        # Load prototype data
        for i in self._all_ids():
            _type = UwApi.prototype_type(i)
            js_str = UwApi.prototype_json(i)
            
            # Skip if JSON data is missing
            if not js_str:
                continue
                
            # Parse JSON data
            try:
                js = json.loads(js_str)
            except json.JSONDecodeError:
                self._game.log_warning(f"Failed to parse JSON for prototype {i}")
                continue
                
            # Skip if name is missing
            if "name" not in js:
                continue
                
            # Store prototype data by type
            if _type == PrototypeTypeEnum.Resource:
                self._resources[i] = js
            elif _type == PrototypeTypeEnum.Recipe:
                self._recipes[i] = js
            elif _type == PrototypeTypeEnum.Construction:
                self._constructions[i] = js
            elif _type == PrototypeTypeEnum.Unit:
                self._units[i] = js
                
            # Store generic prototype data
            self._types[i] = ProtoGeneric(_type, js["name"], js)
            self._all.append(i)
            
        self._game.log_info(f"Loaded {len(self._all)} prototypes")
        
    def _load_definitions(self):
        """Load game definitions."""
        self._game.log_info("Loading definitions...")
        
        # Get definitions JSON
        defs_str = UwApi.definitions_json()
        if not defs_str:
            self._game.log_warning("Failed to get definitions JSON")
            return
            
        # Parse definitions JSON
        try:
            defs = json.loads(defs_str)
        except json.JSONDecodeError:
            self._game.log_warning("Failed to parse definitions JSON")
            return
            
        # Store definitions data
        if "hitChancesTable" in defs:
            self._hit_chances_table = defs["hitChancesTable"]
        if "terrainTypesTable" in defs:
            self._terrain_types_table = defs["terrainTypesTable"]
            
        self._game.log_info("Definitions loaded")
        
    def _map_state_changed(self, state: MapStateEnum):
        """Handle map state changes."""
        if state == MapStateEnum.Loaded:
            self._load_prototypes()
            self._load_definitions()
