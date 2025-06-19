import os
import random
import uw


class Bot:
    def __init__(self):
        self.game = uw.Game()
        self.step = 0

        # register update callback
        self.game.add_update_callback(self.update_callback_closure())

    def start(self):
        self.game.log_info("Starting bot...")
        self.game.set_player_name("bot-py")
        
        # Try to reconnect to existing game
        if not self.game.try_reconnect():
            # Start a new game
            self.game.set_start_gui(True)
            
            # Check for connection parameters
            lobby = os.environ.get("UNNATURAL_CONNECT_LOBBY", "")
            addr = os.environ.get("UNNATURAL_CONNECT_ADDR", "")
            port = os.environ.get("UNNATURAL_CONNECT_PORT", "")
            
            # Connect based on available parameters
            if lobby != "":
                self.game.log_info(f"Connecting to lobby {lobby}...")
                self.game.connect_lobby_id(int(lobby))
            elif addr != "" and port != "":
                self.game.log_info(f"Connecting to {addr}:{port}...")
                self.game.connect_direct(addr, int(port))
            else:
                self.game.log_info("Starting new server...")
                self.game.connect_new_server()
                
        self.game.log_info("Bot started successfully")

    def attack_nearest_enemies(self):
        """Command all combat units to attack the nearest enemy."""
        # Find all player-owned units with combat capability
        own_units = [
            e
            for e in self.game.world.entities().values()
            if e.own()
            and e.has("Unit")
            and self.game.prototypes.unit(e.Proto.proto)
            and self.game.prototypes.unit(e.Proto.proto).get("dps", 0) > 0
        ]
        if not own_units:
            return

        # Find all enemy units
        enemy_units = [
            e
            for e in self.game.world.entities().values()
            if e.policy() == uw.Policy.Enemy and e.has("Unit")
        ]
        if not enemy_units:
            return

        # Order each unit to attack the nearest enemy
        for unit in own_units:
            unit_id = unit.Id
            unit_pos = unit.Position.position
            
            # Only issue orders if the unit doesn't already have orders
            if len(self.game.commands.orders(unit_id)) == 0:
                # Find nearest enemy
                nearest_enemy = sorted(
                    enemy_units,
                    key=lambda x: self.game.map.distance_estimate(
                        unit_pos, x.Position.position
                    ),
                )[0]
                
                # Issue attack order
                attack_order = self.game.commands.fight_to_entity(nearest_enemy.Id)
                self.game.commands.order(unit_id, attack_order)

    def assign_random_recipes(self):
        """Assign random recipes to all units that can use them."""
        for entity in self.game.world.entities().values():
            # Check if entity is a player-owned unit
            if not (entity.own() and entity.has("Unit")):
                continue
                
            # Get unit prototype
            unit_proto = self.game.prototypes.unit(entity.Proto.proto)
            if not unit_proto:
                continue
                
            # Get available recipes
            recipes = unit_proto.get("recipes", [])
            if recipes:
                # Assign a random recipe
                self.game.commands.command_set_recipe(entity.Id, random.choice(recipes))

    def update_callback_closure(self):
        """Create and return the update callback function."""
        def update_callback(stepping):
            # Only process when the game is stepping (not paused)
            if not stepping:
                return
                
            # Increment step counter
            self.step += 1  # save some cpu cycles by splitting work over multiple steps

            # Issue attack orders every 10 steps
            if self.step % 10 == 1:
                self.attack_nearest_enemies()

            # Assign recipes every 10 steps with offset
            if self.step % 10 == 5:
                self.assign_random_recipes()

        return update_callback


if __name__ == "__main__":
    bot = Bot()
    bot.start()
