import random

from inspect import getmembers

import uw


class Bot:
    def __init__(self, game):
        self.game = game
        self.step = 0

        # register update callback
        self.game.add_update_callback(self.tick_callback_closure())

    def start(self):
        print("starting")
        # game.connect_lobby_id(123)
        if not self.game.try_reconnect():
            self.game.set_start_gui(True)
            if not self.game.set_connect_find_lan():
                self.game.connect_new_server()
        print("done")

    def attack_nearest_enemies(self):
        own_units = [e for e in self.game.world.entities().values() if
                     e.own() and e.has("Unit") and self.game.prototypes.unit(e.Proto.proto) and
                     self.game.prototypes.unit(e.Proto.proto).get("dps", 0) > 0]
        if not own_units:
            return

        enemy_units = [e for e in self.game.world.entities().values() if
                       e.policy() == uw.Policy.Enemy and e.has("Unit")]
        if not enemy_units:
            return

        for u in own_units:
            _id = u.Id
            pos = u.Position.position
            if len(self.game.commands.orders(_id)) == 0:
                enemy = \
                    sorted(enemy_units,
                           key=lambda x: self.game.map.distance_estimate(pos, x.Position.position))[0]
                self.game.commands.order(_id, self.game.commands.fight_to_entity(enemy.Id))

    def assign_random_recipes(self):
        for e in self.game.world.entities().values():
            if not (e.own() and hasattr(e, "Unit")):
                continue
            recipes = self.game.prototypes.unit(e.Proto.proto)
            if not recipes:
                continue
            recipes = recipes["recipes"]
            if len(recipes) > 0:
                self.game.commands.command_set_recipe(e.Id, random.choice(recipes))

    def tick_callback_closure(self):
        def tick_callback(stepping):
            if not stepping:
                return
            self.step += 1

            if self.step % 10 == 1:
                self.attack_nearest_enemies()

            if self.step % 10 == 5:
                self.assign_random_recipes()

        return tick_callback


if __name__ == '__main__':
    # game = uw.Game(steam_path=STEAM_PATH)
    game = uw.Game()
    game.log("Hello from the example bot!")
    game.log("this is a mistake", severity=uw.Severity.Error)
    game.set_player_name("the_best_bot_player")

    bot = Bot(game)
    bot.start()
