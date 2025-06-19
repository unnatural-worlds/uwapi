# High-level API components
from .game import Game
from .commands import Commands, Order
from .map import Map, Vector3
from .prototypes import Prototypes, ProtoGeneric
from .world import World, Entity, Policy

# Expose all enums from interop for backwards compatibility
from .interop import (
    ConnectionStateEnum as ConnectionState,
    GameStateEnum as GameState,
    MapStateEnum as MapState,
    OrderTypeEnum as OrderType,
    OrderPriorityEnum as OrderPriority,
    PriorityEnum as Priority,
    PingEnum as Ping,
    PathStateEnum as PathState,
    ForeignPolicyEnum as ForeignPolicy,
    ChatTargetFlagsEnum as ChatTargetFlags,
    UnitStateFlagsEnum as UnitStateFlags,
    PlayerStateFlagsEnum as PlayerStateFlags,
    PlayerConnectionClassEnum as PlayerConnectionClass,
    ForceStateFlagsEnum as ForceStateFlags,
    TaskTypeEnum as TaskType,
    PrototypeTypeEnum as PrototypeType,
    OverviewFlagsEnum as OverviewFlags,
    SeverityEnum as Severity
)
