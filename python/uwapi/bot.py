import os
import sys
import random
import time

print("Bot script starting...")

# Store the original directory
original_dir = os.getcwd()
print(f"Original directory: {original_dir}")

# Change to the directory with the library files before importing uw
# Look for common locations of the game's bin directory
if sys.platform == 'win32':
    possible_paths = [
        "C:/Program Files (x86)/Steam/steamapps/common/Unnatural Worlds/bin",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Steam", "steamapps", "common", "Unnatural Worlds", "bin")
    ]
elif sys.platform == 'darwin':
    possible_paths = [
        os.path.expanduser("~/.steam/steam/steamapps/common/Unnatural Worlds/bin")
    ]
else:
    possible_paths = [
        os.path.expanduser("~/.steam/steam/steamapps/common/Unnatural Worlds/bin")
    ]

# Add environment variable path if set
if os.environ.get("UNNATURAL_ROOT"):
    possible_paths.insert(0, os.environ.get("UNNATURAL_ROOT"))

# Try each path
lib_dir = None
for path in possible_paths:
    if os.path.exists(path):
        print(f"Changing directory to: {path}")
        os.chdir(path)
        lib_dir = path
        break
else:
    print("Could not find Unnatural Worlds installation directory.")
    print(f"Current directory: {os.getcwd()}")
    print("Continuing with current directory...")

# Now import uw after changing to the correct directory
print("Importing uw module...")
import uw
print("uw module imported successfully")

# Return to original directory for consistent file paths
if lib_dir:
    print(f"Changing back to original directory: {original_dir}")
    os.chdir(original_dir)

print(f"Current working directory: {os.getcwd()}")
print(f"Library directory: {lib_dir}")

class Bot:
    def __init__(self):
        print("Initializing bot...")
        self.game = uw.Game()
        print("Game object created")
        self.step = 0

        # register update callback
        print("Registering update callback...")
        self.game.add_update_callback(self.update_callback_closure())
        print("Update callback registered")
        
    def wait_for_state(self, desired_game_state, max_wait=10, check_interval=0.5):
        """
        Wait for a specific game state for up to max_wait seconds.
        Returns True if the state was reached, False if timed out.
        """
        print(f"Waiting up to {max_wait} seconds for game state: {desired_game_state}")
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            current_state = self.game.game_state()
            current_conn = self.game.connection_state()
            
            print(f"Current states - game: {current_state}, connection: {current_conn}")
            
            if current_state == desired_game_state:
                print(f"Reached desired state: {desired_game_state} after {time.time() - start_time:.1f} seconds")
                return True
                
            time.sleep(check_interval)
            
        print(f"Timed out waiting for state: {desired_game_state}")
        return False

    def start(self):
        print("Starting bot...")
        self.game.log_info("Starting bot...")
        
        # Set up the GUI flag first
        self.game.set_start_gui(True)
        print("GUI enabled")
        
        # Try to reconnect to existing game
        print("Trying to reconnect...")
        reconnected = self.game.try_reconnect()
        
        # If reconnection failed, establish a new connection
        if not reconnected:
            print("Reconnect failed, starting new game")
            
            # Check for connection parameters
            lobby = os.environ.get("UNNATURAL_CONNECT_LOBBY", "")
            addr = os.environ.get("UNNATURAL_CONNECT_ADDR", "")
            port = os.environ.get("UNNATURAL_CONNECT_PORT", "")
            print(f"Connection parameters: lobby={lobby}, addr={addr}, port={port}")
            
            # Connect based on available parameters
            if lobby != "":
                self.game.log_info(f"Connecting to lobby {lobby}...")
                self.game.connect_lobby_id(int(lobby))
            elif addr != "" and port != "":
                self.game.log_info(f"Connecting to {addr}:{port}...")
                self.game.connect_direct(addr, int(port))
            else:
                # Try to connect to localhost as a fallback
                try:
                    self.game.log_info("Trying to connect to localhost:7777...")
                    self.game.connect_direct("localhost", 7777)
                except Exception as e:
                    print(f"Failed to connect to localhost: {e}")
                    self.game.log_info("Starting new server...")
                    try:
                        # Launch with higher visibility in case the localhost one fails
                        self.game.connect_new_server(1, "Bot Server", "--observer 1")
                    except Exception as server_ex:
                        print(f"Failed to start server: {server_ex}")
                        print("Please make sure the game is installed and the server executable is in the correct location.")
        else:
            print("Reconnected to existing game")
        
        # Wait for connection to be established
        print("Waiting for connection to be established...")
        
        # Try to wait for the Session state
        from uw import GameState, ConnectionState
        if self.wait_for_state(GameState.Session, max_wait=10):
            print(f"Game state: {self.game.game_state()}, setting player name...")
            self.game.set_player_name("bot-py")
            print("Player name set")
        else:
            print(f"Timed out waiting for Session state - current state: {self.game.game_state()}, connection: {self.game.connection_state()}")
            print("Will try to set name later when game is ready")
                
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
        def update_callback(tick, stepping=True):
            print(f"Update callback fired - tick: {tick}, stepping: {stepping}")
            # Only process when the game is stepping (not paused)
            if not stepping:
                print("Game is paused, skipping update")
                return
                
            # Increment step counter
            self.step += 1  # save some cpu cycles by splitting work over multiple steps
            print(f"Step: {self.step}")

            # Issue attack orders every 10 steps
            if self.step % 10 == 1:
                print("Attacking nearest enemies")
                self.attack_nearest_enemies()

            # Assign recipes every 10 steps with offset
            if self.step % 10 == 5:
                print("Assigning random recipes")
                self.assign_random_recipes()

        return update_callback


if __name__ == "__main__":
    print("Main script starting...")
    try:
        # Create and start the bot
        bot = Bot()
        print("Bot created, starting...")
        bot.start()
        print("Bot started, entering infinite loop to keep the script running")
        
        # Keep the script running to allow the GUI to run
        name_set = False
        tick_count = 0
        
        while True:
            time.sleep(1)
            tick_count += 1
            
            # If we haven't set the player name yet, check if we can do it now
            if not name_set:
                from uw import GameState
                game_state = bot.game.game_state()
                if game_state == GameState.Session:
                    print(f"Game state is now {game_state}, setting player name...")
                    try:
                        bot.game.set_player_name("bot-py")
                        name_set = True
                        print("Player name set successfully")
                    except Exception as e:
                        print(f"Failed to set player name: {e}")
            
            # Print a status update occasionally
            if tick_count % 10 == 0:  # Every ~10 seconds
                game_state = bot.game.game_state()
                conn_state = bot.game.connection_state()
                print(f"Bot running - Game state: {game_state}, Connection state: {conn_state}")
    except KeyboardInterrupt:
        print("Bot terminated by user")
    except Exception as e:
        print(f"Error in bot: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Bot execution finished")
