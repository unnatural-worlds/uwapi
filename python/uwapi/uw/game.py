import os
from typing import Callable, List, Optional, Dict, Any

from .interop import UwApi, ConnectionStateEnum, GameStateEnum, MapStateEnum, SeverityEnum
from .commands import Commands
from .prototypes import Prototypes
from .map import Map
from .world import World


class Game:
    """Main game interface that provides access to the UW API."""
    
    def __init__(self):
        """Initialize the game interface."""
        self._connection_state_handlers = []
        self._game_state_handlers = []
        self._map_state_handlers = []
        self._update_handlers = []
        self._shooting_handlers = []
        self._force_eliminated_handlers = []
        self._chat_handlers = []
        
        # Initialize component interfaces
        self.prototypes = Prototypes(self)
        self.map = Map(self)
        self.world = World(self)
        self.commands = Commands()
        
        # Register internal callback handlers
        UwApi.add_connection_state_callback(self._connection_state_callback)
        UwApi.add_game_state_callback(self._game_state_callback)
        UwApi.add_map_state_callback(self._map_state_callback)
        UwApi.add_update_callback(self._update_callback)
        UwApi.add_shooting_callback(self._shooting_callback)
        UwApi.add_force_eliminated_callback(self._force_eliminated_callback)
        UwApi.add_chat_callback(self._chat_callback)

        self._tick = 0
        
    def __del__(self):
        """Clean up resources when the game is destroyed."""
        UwApi.shutdown()
        
    # Logging methods
    def log(self, message: str, severity: SeverityEnum = SeverityEnum.Info):
        """Log a message with the specified severity."""
        UwApi.log(severity, message)
        
    def log_info(self, message: str):
        """Log an info message."""
        self.log(message, SeverityEnum.Info)
        
    def log_warning(self, message: str):
        """Log a warning message."""
        self.log(message, SeverityEnum.Warning)
        
    def log_error(self, message: str):
        """Log an error message."""
        self.log(message, SeverityEnum.Error)
        
    # Connection methods
    def set_player_name(self, name: str):
        """Set the player's name."""
        UwApi.set_player_name(name)
        
    def set_player_color(self, r: float, g: float, b: float):
        """Set the player's color."""
        UwApi.set_player_color(r, g, b)
        
    def set_start_gui(self, start_gui: bool, extra_params: str = "--observer 1"):
        """Set whether to start the GUI when connecting."""
        UwApi.set_connect_start_gui(start_gui, extra_params)
        
    def connect_find_lan(self, timeout_us: int = 1000000) -> bool:
        """Find and connect to a LAN server."""
        return UwApi.connect_find_lan(timeout_us)
        
    def connect_direct(self, address: str, port: int):
        """Connect directly to a server by address and port."""
        UwApi.connect_direct(address, port)
        
    def connect_lobby_id(self, lobby_id: int):
        """Connect to a server by lobby ID."""
        UwApi.connect_lobby_id(lobby_id)
        
    def connect_new_server(self, visibility: int = 0, name: str = "", extra_params: str = ""):
        """Create and connect to a new server."""
        UwApi.connect_new_server(visibility, name, extra_params)
        
    def try_reconnect(self) -> bool:
        """Try to reconnect to the last server."""
        return UwApi.try_reconnect()
        
    def disconnect(self):
        """Disconnect from the current server."""
        UwApi.disconnect()
        
    # State methods
    def connection_state(self) -> ConnectionStateEnum:
        """Get the current connection state."""
        return UwApi.connection_state()
        
    def game_state(self) -> GameStateEnum:
        """Get the current game state."""
        return UwApi.game_state()
        
    def map_state(self) -> MapStateEnum:
        """Get the current map state."""
        return UwApi.map_state()
        
    def tick(self) -> int:
        """Get the current game tick."""
        return self._tick
        
    # Callback registration methods
    def add_connection_state_callback(self, callback: Callable[[ConnectionStateEnum], None]):
        """Register a callback for connection state changes."""
        self._connection_state_handlers.append(callback)
        return callback
        
    def add_game_state_callback(self, callback: Callable[[GameStateEnum], None]):
        """Register a callback for game state changes."""
        self._game_state_handlers.append(callback)
        return callback
        
    def add_map_state_callback(self, callback: Callable[[MapStateEnum], None]):
        """Register a callback for map state changes."""
        self._map_state_handlers.append(callback)
        return callback
        
    def add_update_callback(self, callback: Callable[[bool], None]):
        """Register a callback for game updates."""
        self._update_handlers.append(callback)
        return callback
        
    def add_shooting_callback(self, callback: Callable[[List[Any]], None]):
        """Register a callback for shooting events."""
        self._shooting_handlers.append(callback)
        return callback
        
    def add_force_eliminated_callback(self, callback: Callable[[int], None]):
        """Register a callback for force elimination events."""
        self._force_eliminated_handlers.append(callback)
        return callback
        
    def add_chat_callback(self, callback: Callable[[str, int, int], None]):
        """Register a callback for chat messages."""
        self._chat_handlers.append(callback)
        return callback
        
    # Internal callback handlers
    def _connection_state_callback(self, state: ConnectionStateEnum):
        """Handle connection state changes."""
        for handler in self._connection_state_handlers:
            try:
                handler(state)
            except Exception as e:
                self.log_error(f"Error in connection state callback: {e}")
                
    def _game_state_callback(self, state: GameStateEnum):
        """Handle game state changes."""
        for handler in self._game_state_handlers:
            try:
                handler(state)
            except Exception as e:
                self.log_error(f"Error in game state callback: {e}")
                
    def _map_state_callback(self, state: MapStateEnum):
        """Handle map state changes."""
        for handler in self._map_state_handlers:
            try:
                handler(state)
            except Exception as e:
                self.log_error(f"Error in map state callback: {e}")
                
    def _update_callback(self, tick: int, stepping: bool):
        """Handle game updates."""
        self._tick = tick
        for handler in self._update_handlers:
            try:
                handler(stepping)
            except Exception as e:
                self.log_error(f"Error in update callback: {e}")
                
    def _shooting_callback(self, shooting_data: List[Any]):
        """Handle shooting events."""
        if not self._shooting_handlers:
            return
        for handler in self._shooting_handlers:
            try:
                handler(shooting_data)
            except Exception as e:
                self.log_error(f"Error in shooting callback: {e}")
                
    def _force_eliminated_callback(self, force_id: int):
        """Handle force elimination events."""
        for handler in self._force_eliminated_handlers:
            try:
                handler(force_id)
            except Exception as e:
                self.log_error(f"Error in force eliminated callback: {e}")
                
    def _chat_callback(self, message: str, sender: int, target_flags: int):
        """Handle chat messages."""
        for handler in self._chat_handlers:
            try:
                handler(message, sender, target_flags)
            except Exception as e:
                self.log_error(f"Error in chat callback: {e}")
