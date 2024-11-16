
# Smart Home Integration Documentation

The FlipDot panel control project includes advanced smart home functionality, enabling integration with Home Assistant or other MQTT-based systems. This integration allows the FlipDot display to show notifications, time, weather, and other smart home alerts, making it a dynamic element of your smart home environment.

## Key Components

### MQTT Communication
The project uses MQTT to receive commands and data from the smart home system. These commands control the display modes, update messages, and allow interaction with other smart home devices.

### `mqtt_handler.py` and Smart Home Display Updates
The `mqtt_handler.py` script contains multiple functions dedicated to updating the FlipDot display based on MQTT messages. Here are the primary functions related to smart home integration:

1. **`clock_mode(self)`**
   - Activates clock display mode.
   - Shows the current time using the `Clock` object, which supports digital or analog formats.

2. **`push_assets(self)`**
   - Updates the display with the most recent assets or notifications sent from the smart home system.

3. **`callback(self, client, userdata, message)`**
   - Processes incoming MQTT messages and updates the display accordingly.
   - Acts as the central function to switch display modes based on commands.

4. **`play(self, asset_name)`** and **`play_loop(self, asset_name)`**
   - Display single or looping animations in response to MQTT triggers.

### Smart Home Data in JSON Format
The `Clock` and other display modes use JSON-formatted data to structure information received from the smart home system. Here’s an example JSON format from `clock.py`, illustrating a typical setup:

```json
{
    "mode": "clock",
    "design": "digital",
    "time_format": "HH:MM",
    "display_duration": 10
}
```

#### Explanation of JSON Fields
- **`mode`**: Defines the display mode (e.g., "clock" for time display).
- **`design`**: Specifies the clock design (e.g., "digital" or "analog").
- **`time_format`**: Determines the time format (e.g., "HH:MM" or "HH:MM:SS").
- **`display_duration`**: Duration for which the display remains active in this mode.

### Example Configuration in Home Assistant
To integrate the FlipDot panel with Home Assistant, add MQTT sensors and automations that publish commands to the FlipDot's subscribed topics. Here’s an example Home Assistant configuration:

```yaml
mqtt:
  sensor:
    - name: "FlipDot Clock Mode"
      state_topic: "Flipdot/display/mode"
      command_topic: "Flipdot/display/set_mode"
      payload_on: "clock_mode"
      payload_off: "shutdown"

automation:
  - alias: "Update FlipDot Clock"
    trigger:
      - platform: time_pattern
        minutes: "/1"
    action:
      - service: mqtt.publish
        data:
          topic: "Flipdot/display/set_mode"
          payload: "clock_mode"
```

### Usage and Setup

1. **Enable Clock Mode**: Publish a message to the `Flipdot/display/set_mode` topic with `payload: "clock_mode"` to activate clock display.
2. **Display Notifications**: Configure Home Assistant to send alerts or messages to the FlipDot panel using the `callback` function in `mqtt_handler.py`.

---

This setup allows your FlipDot display to respond to smart home events and display relevant data in real-time. The JSON configuration and Home Assistant integration make it adaptable to a variety of smart home scenarios.

### JSON Structure Example for Smart Home Notifications

In addition to the basic configuration, the project supports detailed JSON-based data for dynamic and contextual updates on the FlipDot display.
Here’s an example JSON structure used in `clock.py`, providing various smart home statuses:

```python
if __name__ == "__main__":
    clock = Clock(design="digital")
    frame = "{{"notifications":["shower","tub","flo","kehrstin"],"             ""washer":{{"status":"off","remaining_time":0}},"luften":{{"wozi":"none","esszi":"open"}},"outdoor":{{"temp":21,"hum":65.0}},"             ""forecast":{{"temp":26,"weather":"rainy"}},"fan":{{"Gustav":"unavailable","             ""Venti":"unavailable","Fritz":"unavailable"}},"timer":200,"calender":{{"name":"Linz :)","             ""start_time":"2023-05-16 19:33:00","end_time":"2023-05-15 00:00:00"}},"traffic":{{"bus": "             "{{"departure 3": "6" , "departure 28": "unknown"}},"car": -1,"bike": -1}},"plants":{{"berndt":false,"willhelm":true}}}}"
```

### Explanation of JSON Fields
- **`notifications`**: List of active notifications for the user, such as "shower" or "tub".
- **`washer`**: Contains status (`on` or `off`) and `remaining_time` for a washing machine.
- **`luften`**: Represents ventilation status per room (`wozi` for living room, `esszi` for dining room), showing if windows are open.
- **`outdoor`**: Outdoor environmental data, with `temp` (temperature) and `hum` (humidity).
- **`forecast`**: Weather forecast details, showing temperature and weather condition (e.g., "rainy").
- **`fan`**: Status of fans in the home, with keys for individual fans (`Gustav`, `Venti`, `Fritz`).
- **`timer`**: Generic countdown timer for timed tasks or events.
- **`calender`**: Calendar entry with `name`, `start_time`, and `end_time`.
- **`traffic`**: Transportation information, including bus departure times and estimated car/bike travel times.
- **`plants`**: Status of plant moisture sensors (`true` for healthy, `false` for needing water).

### Example Home Assistant Configuration with Advanced Data
This JSON format can be adapted to provide rich, real-time feedback on the FlipDot display, integrated with Home Assistant’s automation capabilities. For example, send updated data for notifications, weather, and more with:

```yaml
automation:
  - alias: "Update FlipDot Detailed Status"
    trigger:
      - platform: time_pattern
        minutes: "/5"
    action:
      - service: mqtt.publish
        data:
          topic: "Flipdot/display/update"
          payload: "{{ frame }}"  # Replace `frame` with dynamically generated JSON
```

This setup provides comprehensive, dynamic information to the FlipDot display, enhancing the smart home experience.
