
# FlipDot Panel Control Project

This project is a Python-based system to control FlipDot panels using MQTT for integration with a smart home setup, particularly Home Assistant. The project consists of multiple components, each responsible for different functionalities, such as designing animations, displaying images, or running interactive modes like games and visualizations.

## Project Structure

The project is organized into two main parts and some experiments:

1. **Raspberry Pi Controller**
   - **Entry Point**: `mqtt_handler.py`
   - **Description**: Manages MQTT communication, handles file storage, and operates various display modes (e.g., clock, animations).
   - **Core Functionality**: Acts as the central controller to process MQTT messages and update the FlipDot display.

2. **PC Animation Designer**
   - **Main Script**: `Designer.py`
   - **Description**: A design tool to create and preview animations and images, which can then be sent to the Raspberry Pi for display.

3. **Experiments**
   - **LiveMode.py**: Allows for casting live input (e.g., camera feed) to the FlipDot display.
   - **Music.py**: Integrates MIDI controllers for interactive music visualizations.

## Hardware Requirements
- **Raspberry Pi** (any model with GPIO support)
- **RS485 Shield** for communication with FlipDot panels
- **FlipDot Panels** that support RS485

## Installation

### 1. Set Up the Raspberry Pi
- Install Raspberry Pi OS.
- Connect to WiFi or Ethernet for MQTT communication.

### 2. Install Required Libraries
Run the following commands on the Raspberry Pi to install the necessary Python libraries:

```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

## Main Scripts and Their Roles

- **`mqtt_handler.py`**: Acts as the central controller, handling display modes, managing files, and integrating smart home features.
- **`Designer.py`**: Provides a GUI for creating animations on a PC.
- **`LiveMode.py`** and **`Music.py`**: Experimental scripts for live interaction using external devices.

## Configuration and Setup

### MQTT Configuration
- **Config File**: `mqtt_config.cfg`
- **Format**:
  ```json
  {
      "broker": "homeassistant.local",
      "port": 1883,
      "user": "your_username",
      "password": "your_password"
  }
  ```

## Usage Instructions

### Running the Controller on the Raspberry Pi
- Start `mqtt_handler.py` to connect the FlipDot panel to MQTT and enable display functionality.
- Use Home Assistant or other MQTT publishers to send commands and updates to the display.

### Using the Designer
- Run `Designer.py` on a PC to create animations or images, then upload them to the Raspberry Pi for display.

### Experiment Modes
- **LiveMode.py**: Cast live camera input to the FlipDot display using an Android device.
- **Music.py**: Integrate a MIDI controller to display real-time visualizations in response to audio.

---

This setup allows the FlipDot panel to function as a dynamic display within a smart home, showing time, notifications, animations, and interactive games.

