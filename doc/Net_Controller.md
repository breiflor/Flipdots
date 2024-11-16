
# `Net_Controller` Class Documentation

The `Net_Controller` class in `mqtt_handler.py` manages the MQTT communication, display control, and smart home functionality for the FlipDot panel system. It supports advanced features like mode switching, file management, and interactive display elements.

## Class Overview
- **File**: `mqtt_handler.py`
- **Primary Function**: Control the FlipDot panels, manage MQTT commands, and handle display modes and file management.

## Methods

### `__init__(self, broker='homeassistant.local', port=1883, client_id='Fliptot watchdog', settings='mqtt_config.cfg')`
- Initializes the controller with broker and port settings, loads MQTT configuration, initializes display objects, and subscribes to MQTT topics.

### `on_connect(self, client, userdata, flags, rc)`
- Handles MQTT connection events and sets up actions upon connection.

### `callback(self, client, userdata, message)`
- Processes received MQTT messages to control the display or change display modes.

### `subcribe(self, topic, func)`
- Allows dynamic MQTT topic subscription with a specified callback.

### `shutdown(self)`
- Shuts down the FlipDot display, clearing or turning off panels.

### `live_mode(self)`
- Activates live mode for dynamic display of external input.

### `add_animation(self, animation)`
- Adds a new animation to the display queue.

### `add_image(self, image)`
- Adds a static image to the display queue.

### `remove_asset(self, asset_name)`
- Removes a specified asset from the system.

### `play(self, asset_name)`
- Plays a specified asset once.

### `play_loop(self, asset_name)`
- Loops a specified asset until interrupted.

### `clock_mode(self)`
- Switches display to clock mode to show time.

### `music_mode(self)`
- Activates music mode for visualizations responding to audio.

### `run_state_machine(self)`
- Manages state transitions between display modes.

### `push_assets(self)`
- Pushes assets to the display to update content.

### `blacklisted(self, asset_name)`
- Checks if an asset is blacklisted.

### `load_game(self, game_name)`
- Loads a specific game on the display.

### `send_image(self, image_data)`
- Sends image data for immediate display.

### `send_animation(self, animation_data)`
- Sends animation data for immediate playback.

---

This class enables comprehensive control of the FlipDot display system, integrating MQTT for remote command handling and display management.
