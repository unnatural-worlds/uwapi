from typing import List, Optional
from dataclasses import dataclass

from .interop import UwApi, OrderTypeEnum, OrderPriorityEnum, PriorityEnum, UwOrder


@dataclass
class Order:
    """Represents an order that can be issued to a unit."""
    entity: int
    position: int
    order_type: OrderTypeEnum
    priority: OrderPriorityEnum


class Commands:
    """Provides methods for issuing commands to units in the game."""
    
    # Invalid entity or position ID
    invalid = 4294967295
    
    def orders(self, unit: int) -> List[Order]:
        """Get all orders for a unit."""
        orders_data = UwApi.orders(unit)
        if not orders_data or not hasattr(orders_data, 'orders'):
            return []
            
        result = []
        for order in orders_data.orders:
            result.append(Order(
                entity=order.entity,
                position=order.position,
                order_type=OrderTypeEnum(order.order),
                priority=OrderPriorityEnum(order.priority)
            ))
        return result
        
    def order(self, unit: int, order: Order):
        """Issue an order to a unit."""
        # Create order object
        order_obj = UwOrder(
            entity=order.entity,
            position=order.position,
            order=int(order.order_type),
            priority=int(order.priority)
        )
        UwApi.order(unit, order_obj)
        
    def stop(self) -> Order:
        """Create a stop order."""
        return Order(
            entity=self.invalid,
            position=self.invalid,
            order_type=OrderTypeEnum.Stop,
            priority=OrderPriorityEnum.User
        )
        
    def guard(self) -> Order:
        """Create a guard order."""
        return Order(
            entity=self.invalid,
            position=self.invalid,
            order_type=OrderTypeEnum.Guard,
            priority=OrderPriorityEnum.User
        )
        
    def run_to_position(self, position: int) -> Order:
        """Create an order to run to a position."""
        return Order(
            entity=self.invalid,
            position=position,
            order_type=OrderTypeEnum.Run,
            priority=OrderPriorityEnum.User
        )
        
    def run_to_entity(self, entity: int) -> Order:
        """Create an order to run to an entity."""
        return Order(
            entity=entity,
            position=self.invalid,
            order_type=OrderTypeEnum.Run,
            priority=OrderPriorityEnum.User
        )
        
    def fight_to_position(self, position: int) -> Order:
        """Create an order to fight at a position."""
        return Order(
            entity=self.invalid,
            position=position,
            order_type=OrderTypeEnum.Fight,
            priority=OrderPriorityEnum.User
        )
        
    def fight_to_entity(self, entity: int) -> Order:
        """Create an order to fight an entity."""
        return Order(
            entity=entity,
            position=self.invalid,
            order_type=OrderTypeEnum.Fight,
            priority=OrderPriorityEnum.User
        )
        
    # Direct command methods
    
    def command_self_destruct(self, unit: int):
        """Command a unit to self-destruct."""
        UwApi.command_self_destruct(unit)
        
    def command_place_construction(self, proto: int, position: int, yaw: float = 0):
        """Command to place a construction."""
        UwApi.command_place_construction(proto, position, yaw, 0, PriorityEnum.Normal)
        
    def command_set_recipe(self, unit: int, recipe: int):
        """Set the recipe for a unit."""
        UwApi.command_set_recipe(unit, recipe)
        
    def command_set_priority(self, unit: int, priority: PriorityEnum):
        """Set the priority for a unit."""
        UwApi.command_set_priority(unit, priority)
        
    def command_load(self, unit: int, resource_type: int):
        """Command a unit to load a resource."""
        UwApi.command_load(unit, resource_type)
        
    def command_unload(self, unit: int):
        """Command a unit to unload resources."""
        UwApi.command_unload(unit)
        
    def command_move(self, unit: int, position: int, yaw: float = 0):
        """Command a unit to move to a position."""
        UwApi.command_move(unit, position, yaw)
        
    def command_aim(self, unit: int, target: int):
        """Command a unit to aim at a target."""
        UwApi.command_aim(unit, target)
        
    def command_renounce_control(self, unit: int):
        """Renounce control of a unit."""
        UwApi.command_renounce_control(unit)
