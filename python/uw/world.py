#     using Controller = Interop.UwControllerComponent;
#     using Position = Interop.UwPositionComponent;
#     using Unit = Interop.UwUnitComponent;
#     using Life = Interop.UwLifeComponent;
#     using Move = Interop.UwMoveComponent;
#     using Aim = Interop.UwAimComponent;
#     using Recipe = Interop.UwRecipeComponent;
#     using UpdateTimestamp = Interop.UwUpdateTimestampComponent;
#     using RecipeStatistics = Interop.UwRecipeStatisticsComponent;
#     using Amount = Interop.UwAmountComponent;
#     using Attachment = Interop.UwAttachmentComponent;
#     using Player = Interop.UwPlayerComponent;
#     using Force = Interop.UwForceComponent;
#     using ForceDetails = Interop.UwForceDetailsComponent;
#     using ForeignPolicy = Interop.UwForeignPolicyComponent;
#     using DiplomacyProposal = Interop.UwDiplomacyProposalComponent;
#     using PolicyEnum = Interop.UwForeignPolicyEnum;
#
from typing import Any
from enum import Enum


class Policy(Enum):
    NONE = 0
    Self = 1
    Ally = 2
    Neutral = 3
    Enemy = 4


class Object:
    pass


class Entity:
    @staticmethod
    def has(entity: dict[str, Any], component: str):
        return component in entity


#         public static bool Has(dynamic entity, string component)
#         {
#             return ((IDictionary<string, object>)entity).ContainsKey(component);
#         }
#
#         public static bool Has(dynamic entity, IEnumerable<string> components)
#         {
#             foreach (var c in components)
#                 if (!Has(entity, c))
#                     return false;
#             return true;
#         }
#
#         public static bool Own(dynamic entity)
#         {
#             return Has(entity, "Owner") && entity.Owner.force == World.MyForce();
#         }
#
#         public static PolicyEnum Policy(dynamic entity)
#         {
#             if (!Has(entity, "Owner"))
#                 return PolicyEnum.None;
#             return World.Policy(entity.Owner.force);
#         }

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

    @staticmethod
    def policy(force: int) -> Policy:
        return Policy(force) if force in Policy._value2member_map_ else Policy.NONE

    def all_ids(self) -> list[int]:
        ids = self._ffi.new("struct UwIds *")
        self._api.uwAllEntities(ids)
        return self._ffi.unpack(ids)

    def modified_ids(self) -> list[int]:
        ids = self._ffi.new("struct UwIds *")
        self._api.uwModifiedEntities(ids)
        return self._ffi.unpack(ids)

    def _update_removed(self):
        all_ids = set(self.all_ids())
        removed = []
        for _id in self._entities.keys():
            if id in all_ids:
                removed.append(_id)
        for _id in removed:
            del self._entities[_id]

    def _maybe_assign_or_remove(self, e, o, fetch_method):
        struct = fetch_method.replace("Fetch", "")
        field = fetch_method.replace("UwFetch", "").replace("Component", "")
        tmp = self._ffi.new(f"struct {struct} *")
        if getattr(self._api, fetch_method)(e, tmp):
            setattr(o, field, tmp)
        else:
            if hasattr(o, field):
                delattr(o, field)

    def _update_modified(self):
        for _id in self.modified_ids():
            o = self._entities.get(_id, Object())
            o.id = _id
            self._entities[_id] = o
            e = self._ffi.new("struct uwEntityPointer *", _id)

            self._maybe_assign_or_remove(e, o, "UwFetchProtoComponent")
            self._maybe_assign_or_remove(e, o, "UwFetchOwnerComponent")
            self._maybe_assign_or_remove(e, o, "UwFetchControllerComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchControllerComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchPositionComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchUnitComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchLifeComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchMoveComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchAimComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchRecipeComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchUpdateTimestampComponent")
            self._maybe_assign_or_remove(e, o, "uwFetchRecipeStatisticsComponent")
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
            if "ForeignPolicy" not in e:
                continue
            fp = e["ForeignPolicy"]
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
