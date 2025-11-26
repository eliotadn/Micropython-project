# 🕒 ESP32 IoT Smart Clock

This project is a multifunction smart clock based on an ESP32 (FireBeetle). It displays time synchronized via the internet (NTP), environmental data (Temperature/Humidity), and features a menu system navigable via a rotary encoder.

## 🚀 Features

* **Accurate Time**: Automatic synchronization via WiFi (NTP).
* **Environmental Sensors**: Temperature and Humidity reading via DHT12.
* **User Interface**: SH1106 OLED Display managed by a rotary encoder.
* **Menus**:
    1.  Time & Alarm.
    2.  Indoor Weather (Temp/Hum).
    3.  Air Quality (Placeholder for future extension).
* **Alarm**: Audible (Buzzer) and visual (LED) notification.

## 🛠 Hardware Requirements

* **Microcontroller**: ESP32 (FireBeetle model or compatible).
* **Display**: 1.3" OLED Screen (SH1106 Driver) - I2C Interface.
* **Sensor**: DHT12 (Temperature & Humidity) - I2C Interface.
* **Input**: Rotary Encoder (Ky-040 or similar).
* **Outputs**: Passive Buzzer, LED.

## 🔌 Wiring (Pinout)

Here is the complete connection table between the ESP32 and the components.

| Component | Component Pin | ESP32 Pin (GPIO) | Function |
| :--- | :--- | :--- | :--- |
| **I2C Bus** | SDA | **GPIO 21** | Data (Screen + DHT12) |
| | SCL | **GPIO 22** | Clock (Screen + DHT12) |
| **Power** | VCC | **3V3** | System Power |
| | GND | **GND** | Common Ground |
| **Encoder** | CLK (A) | **GPIO 18** | Rotation A |
| | DT (B) | **GPIO 19** | Rotation B |
| | SW (Switch) | **GPIO 4** | Push Button (Click) |
| **Actuators** | LED | **GPIO 2** | Alarm Indicator |
| | Buzzer | **GPIO 27** | Beeper |

> **Note**: The I2C bus (GPIO 21 & 22) is shared. The OLED screen and the DHT12 sensor must be connected to these same pins in parallel.
>
> 
## 📂 Project Structure

The code is modular to facilitate maintenance:

* `Main.py`: Entry point. Initializes hardware and manages the main loop.
* `Clock.py`: Manages WiFi connection and NTP synchronization.
* `Screen_UI.py`: Handles drawing the graphical interface on the OLED.
* `temp_censor.py`: Driver for reading the DHT12 sensor.
* `Lib/`: Folder containing external libraries (`sh1106.py`, `rotary_irq.py`).

## ⚙️ Installation and Configuration

### 1. Prerequisites
* Install **Python** and an IDE (Thonny IDE or VS Code with Pymakr extension).
* Flash **MicroPython** firmware onto the ESP32.

### 2. File Installation
Copy all `.py` files and the `Lib` folder to the root of the ESP32.

### 3. WiFi Configuration
Open the `Clock.py` file and modify the following lines with your credentials:

```python
WIFI_SSID = "YOUR_SSID"
WIFI_PSK  = "YOUR_PASSWORD"
TZ_OFFSET_H = 1  # Adjust according to your time zone (e.g., 1 for CET, 2 for CEST)
