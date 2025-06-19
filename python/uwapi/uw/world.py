from typing import Dict, List, Optional, Any
from enum import Enum

from .interop import UwApi, _unpack_list, Entity as ApiEntity, ForeignPolicyEnum


class Policy(Enum):
    NONE = 0
    Self = 1
    Ally = 2
    Neutral = 3
    Enemy = 4


class Entity:
    """Enhanced entity class with world context."""
    def __init__(self, world, id: int = 0):
        self.Id = id
        self._world = world
        self._api_entity = ApiEntity(id) if id > 0 else None
        
    def has(self, component: str) -> bool:
        """Check if entity has a specific component."""
        return hasattr(self, component)
        
    def own(self) -> bool:
        """Check if this entity is owned by the player."""
        return self.has("Owner") and self.Owner.force == self._world.my_force()
        
    def policy(self) -> Policy:
        """Get the policy status of this entity (ally, enemy, etc.)."""
        if not self.has("Owner"):
            return Policy.NONE
            
        return self._world.policy(self.Owner.force)
        
    def update(self) -> "Entity":
        """Update all components of this entity."""
        if self._api_entity:
            self._api_entity.update()
            # Copy component data from API entity to this entity
            for attr_name in dir(self._api_entity):
                if not attr_name.startswith('_') and attr_name not in ('Id', 'update', 'has', 'own', 'policy', 'fetch_components'):
                    setattr(self, attr_name, getattr(self._api_entity, attr_name))
        return self


class World:
    """Manages the game world and entity tracking."""
    def __init__(self, game):
        """Initialize the world manager.
        
        Args:
            game: The game instance
        """
        self._game = game
        self._my_force: int = 0
        self._entities: Dict[int, Entity] = {}
        self._policies: Dict[int, Policy] = {}
        
        # Register for updates
        self._game.add_update_callback(self._updating)
        
    def my_force(self) -> int:
        """Get the player's force ID."""
        return self._my_force
        
    def entities(self) -> Dict[int, Entity]:
        """Get all entities in the world."""
        return self._entities
        
    def entity(self, _id: int) -> Entity:
        """Get a specific entity by ID."""
        return self._entities[_id]
        
    def policy(self, force: int) -> Policy:
        """Get the policy towards a specific force."""
        return self._policies.get(force, Policy.NONE)
        
    def _all_ids(self) -> List[int]:
        """Get IDs of all entities in the world."""
        return UwApi.all_entities()
        
    def _modified_ids(self) -> List[int]:
        """Get IDs of recently modified entities."""
        return UwApi.modified_entities()
        
    def _update_removed(self):
        """Remove entities that no longer exist."""
        all_ids = set(self._all_ids())
        removed = []
        for _id in self._entities.keys():
            if _id not in all_ids:
                removed.append(_id)
        for _id in removed:
            del self._entities[_id]
            
    def _update_modified(self):
        """Update all modified entities."""
        for _id in self._modified_ids():
            # Get or create entity
            entity = self._entities.get(_id)
            if not entity:
                entity = Entity(self, _id)
                self._entities[_id] = entity
                
            # Update entity components
            entity.update()
            
    def _update_policies(self):
        """Update foreign policies between forces."""
        self._policies = {}
        for e in self._entities.values():
            if not hasattr(e, "ForeignPolicy"):
                continue
                
            fp = getattr(e, "ForeignPolicy")
            # Convert enum values to Policy enum
            if fp.policy == ForeignPolicyEnum.Ally:
                policy = Policy.Ally
            elif fp.policy == ForeignPolicyEnum.Enemy:
                policy = Policy.Enemy
            elif fp.policy == ForeignPolicyEnum.Neutral:
                policy = Policy.Neutral
            elif fp.policy == ForeignPolicyEnum.Self:
                policy = Policy.Self
            else:
                policy = Policy.NONE
                
            # Update policies between forces
            if fp.forces[0] == self._my_force:
                self._policies[fp.forces[1]] = policy
            if fp.forces[1] == self._my_force:
                self._policies[fp.forces[0]] = policy
                
    def _updating(self, stepping: bool):
        """Update callback triggered by the game."""
        if not stepping:
            return
            
        # Get player force
        player = UwApi.my_player()
        if player:
            self._my_force = player.forceEntityId
            
        # Update entities
        self._update_removed()
        self._update_modified()
        self._update_policies()
