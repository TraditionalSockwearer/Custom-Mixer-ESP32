# Custom Audio Mixer (v1.0)

This project uses an ESP32 to read 5 linear faders and 2 rotary encoders, displaying real-time volume levels on individual OLED screens.

## BOM

Here is the complete list of hardware required to build this board.

### Core Electronics
| Component | Quantity | Description | Part Number / Note |
| :--- | :--- | :--- | :--- |
| **Microcontroller** | 1 | ESP32-DevKitC V4 | `ESP32-DEVKITC-32E` |
| **Faders** | 5 | 60mm Slide Potentiometer | `Bourns PTA6043-2015CPB103` |
| **Encoders** | 2 | Rotary Encoder w/ Push Button | `PEC11R-4215F-S0024` |
| **Screens** | 5 | 0.91" OLED Display (I2C) | `Generic 128x32 SSD1306` |
| **Multiplexer** | 1 | I2C Multiplexer (8-Channel) | `TCA9548A Breakout Board` |

### Passive Components
| Component | Quantity | Value | Note |
| :--- | :--- | :--- | :--- |
| **Resistors** | 2 | 10kΩ (1/4W) | I2C Pull-ups |
| **Capacitors** | 11 | 0.1µF (100nF) | Ceramic X7R (Noise Filtering) |
| **Capacitor** | 1 | 100µF (25V) | Electrolytic (Power Smoothing) |

### Mechanical & Hardware
* **PCB:** Custom 2-layer board (Gerbers included in `/hardware` folder).
* **Headers:** 2.54mm Female Header Strips (for mounting ESP32/Screens).
* **Knobs:** 5x Fader Caps (4mm lever), 2x Encoder Knobs (6mm D-Shaft).
* **Screws:** M2x5mm (for faders), M3x6mm (for PCB mounting).
