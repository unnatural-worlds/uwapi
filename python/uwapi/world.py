from .interop import *
from .events import uw_events
from .entity import Entity
from .entity_update_components import entity_update_components


def _make_empty_UwMyForceStatistics() -> UwMyForceStatistics:
    return UwMyForceStatistics(0, 0, 0, 0, 0, 0)


class World:
    _instance = None
    _my_force_id: int = 0
    _my_force_statistics = _make_empty_UwMyForceStatistics()
    _entities: dict[int, Entity] = {}
    _policies: dict[int, UwForeignPolicyEnum] = {}
    _overview: list[UwOverviewFlags] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            uw_events.on_update(cls._instance._update)
        return cls._instance

    def my_force_id(self) -> int:
        return self._my_force_id

    def my_force_statistics(self) -> UwMyForceStatistics:
        return self._my_force_statistics

    def unit_path_state(self, unit_id: int) -> UwPathStateEnum:
        return uw_interop.uwUnitPathState(unit_id)

    def unit_upgrades(self, unit_id: int) -> UwUnitUpgrades:
        return uw_interop.uwUnitUpgrades(unit_id)

    def test_shooting(self, shooter_id: int, target_id: int) -> bool:
        return uw_interop.uwTestShootingEntities(shooter_id, target_id)

    def test_construction_placement(
        self, construction_proto: int, position: int, recipe_proto: int = 0
    ) -> bool:
        return uw_interop.uwTestConstructionPlacement(
            construction_proto, position, recipe_proto
        )

    def find_construction_placement(
        self, construction_proto: int, position: int, recipe_proto: int = 0
    ) -> int:
        return uw_interop.uwFindConstructionPlacement(
            construction_proto, position, recipe_proto
        )

    def overview_flags_all(self) -> list[UwOverviewFlags]:
        return self._overview

    def overview_flags(self, position: int) -> UwOverviewFlags:
        return self._overview[position]

    def overview_entities(self, position: int) -> list[int]:
        return uw_interop.uwOverviewIds(position).ids

    def entities(self) -> dict[int, Entity]:
        return self._entities

    def entity(self, entity_id: int) -> Entity:
        return self._entities[entity_id]

    def policy(self, force_id: int) -> UwForeignPolicyEnum:
        return self._policies.get(force_id, UwForeignPolicyEnum.Nothing)

    def _all_ids(self) -> list[int]:
        return uw_interop.uwAllEntities().ids

    def _modified_ids(self) -> list[int]:
        return uw_interop.uwModifiedEntities().ids

    def _update_removed(self) -> None:
        all_ids = set(self._all_ids())
        removed = [eid for eid in self._entities if eid not in all_ids]
        for eid in removed:
            self._entities[eid].destroyed = True
            self._entities.pop(eid, None)

    def _update_fresh(self) -> None:
        for e in self._entities.values():
            e.fresh = False

    def _update_modified(self) -> None:
        for eid in self._modified_ids():
            if eid in self._entities:
                entity_update_components(self._entities[eid])
            else:
                e = Entity(eid)
                entity_update_components(e)
                self._entities[eid] = e

    def _update_policies(self) -> None:
        self._policies.clear()
        for e in self._entities.values():
            if not e.ForeignPolicy:
                continue
            fp = e.ForeignPolicy
            if fp.forces[0] == self._my_force_id:
                self._policies[fp.forces[1]] = fp.policy
            if fp.forces[1] == self._my_force_id:
                self._policies[fp.forces[0]] = fp.policy

    def _update_overview(self, stepping: bool) -> None:
        if stepping:
            self._overview = uw_interop.uwOverviewExtract().flags
        else:
            self._overview = []

    def _update(self, stepping: bool) -> None:
        tmp = uw_interop.uwMyPlayer()
        self._my_force_id = tmp[1].forceEntityId if tmp[0] else 0
        self._my_force_statistics = uw_interop.uwMyForceStatistics()
        self._update_removed()
        self._update_fresh()
        self._update_modified()
        self._update_policies()
        self._update_overview(stepping)


uw_world = World()
