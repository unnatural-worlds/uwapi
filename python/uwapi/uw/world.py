from typing import Any
from enum import Enum

from .helpers import _unpack_list


class Policy(Enum):
    NONE = 0
    Self = 1
    Ally = 2
    Neutral = 3
    Enemy = 4


class Entity:
    def __init__(self, world):
        self._world = world

    def has(self, component: str):
        return hasattr(self, component)

    def own(self) -> bool:
        return self.has("Owner") and self.Owner.force == self._world.my_force()

    def policy(self) -> Policy:
        if not self.has("Owner"):
            return Policy.NONE

        return self._world.policy(self.Owner.force)


class World:
    def __init__(self, api, ffi, game):
        self._api = api
        self._ffi = ffi
        self._game = game

        self._my_force: int = 0
        self._entities: dict[int, Any] = {}
        self._policies: dict[int, Policy] = {}

        self._game.add_update_callback(self._updating)

    def my_force(self) -> int:
        return self._my_force

    def entities(self) -> dict[int, Any]:
        return self._entities

    def entity(self, _id: int) -> Any:
        return self._entities[_id]

    def policy(self, force: int) -> Policy:
        return self._policies.get(force, Policy.NONE)

    def _all_ids(self) -> list[int]:
        ids = self._ffi.new("struct UwIds *")
        self._api.uwAllEntities(ids)
        return _unpack_list(self._ffi, ids)

    def _modified_ids(self) -> list[int]:
        ids = self._ffi.new("struct UwIds *")
        self._api.uwModifiedEntities(ids)
        return _unpack_list(self._ffi, ids)

    def _update_removed(self):
        all_ids = set(self._all_ids())
        removed = []
        for _id in self._entities.keys():
            if _id not in all_ids:
                removed.append(_id)
        for _id in removed:
            del self._entities[_id]

    def _maybe_assign_or_remove(self, e, o, fetch_method):
        struct = fetch_method.replace("uwFetch", "Uw")
        field = fetch_method.replace("uwFetch", "").replace("Component", "")
        tmp = self._ffi.new(f"struct {struct} *")
        if getattr(self._api, fetch_method)(e, tmp):
            setattr(o, field, tmp)
        else:
            if hasattr(o, field):
                delattr(o, field)

    def _update_modified(self):
        for _id in self._modified_ids():
            o = self._entities.get(_id, Entity(self))
            o.Id = _id
            self._entities[_id] = o
            e = self._api.uwEntityPointer(_id)

            self._maybe_assign_or_remove(e, o, "uwFetchProtoComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchOwnerComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchControllerComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchPositionComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchUnitComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchLifeComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchMoveComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchAimComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchRecipeComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchUpdateTimestampComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchRecipeStatisticsComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchPriorityComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchAmountComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchAttachmentComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchPlayerComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchForceComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchForceDetailsComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchForeignPolicyComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchDiplomacyProposalComponent")

    def _update_policies(self):
        self._policies = {}
        for e in self._entities.values():
            if not hasattr(e, "ForeignPolicy"):
                continue
            fp = getattr(e, "ForeignPolicy")
            forces = self._ffi.unpack(fp.forces, 2)
            policy = Policy(fp.policy)
            if forces[0] == self._my_force:
                self._policies[forces[1]] = policy
            if forces[1] == self._my_force:
                self._policies[forces[0]] = policy

    def _updating(self, stepping: bool):
        player = self._ffi.new("struct UwMyPlayer *")
        self._api.uwMyPlayer(player)
        self._my_force = player.forceEntityId

        self._update_removed()
        self._update_modified()
        self._update_policies()
