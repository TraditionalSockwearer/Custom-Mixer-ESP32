# Custom Mixer ESP32 (v1.0)

This project uses an ESP32 to read 5 linear faders and 2 rotary encoders, displaying real-time volume levels for specific apps, chosen via the rotary encoder, on individual OLED screens.

This project's purpose is to act as a mixer and control the volume of an app when it sounds too loud or too quiet.

The Rotary Encoders will be used as a selecter to scroll through the apps that are active and which slider it should be on.

## Schematic
<img width="3507" height="2480" alt="image" src="https://github.com/user-attachments/assets/8e63d87b-bb34-4a7e-8cb1-daa19f77bfc7" />

## PCB
<img width="2339" height="1654" alt="Custom-Mixer-ESP32__Assembly-1" src="https://github.com/user-attachments/assets/4220ee8c-4c0b-4d28-b14d-0e455bd935e9" />
<img width="2339" height="1654" alt="Custom-Mixer-ESP32__Assembly-2" src="https://github.com/user-attachments/assets/520d193d-56cb-4b02-b0af-01bc3dbfce2b" />

## CAD

<img width="1009" height="692" alt="image" src="https://github.com/user-attachments/assets/92b0a3ab-a96d-406b-9078-12e40f6231f7" />
<img width="1066" height="631" alt="image" src="https://github.com/user-attachments/assets/0cc36be9-2635-4fe2-82b4-069f2975f3ff" />

## BOM

The complete list of hardware required to build this board.
### Core Electronics
| Component | Quantity | Description | Part Number| Link |
| :--- | :--- | :--- | :--- | :--- |
| **Microcontroller** | 1 | ESP32-DevKitC V4 | `ESP32-DEVKITC-32E` | `https://www.digikey.co.uk/en/products/detail/espressif-systems/ESP32-DEVKITC-32E/12091810` |
| **Faders** | 5 | 60mm Slide Potentiometer | `Bourns PTA6043-2015CPB103` | `https://www.digikey.co.uk/en/products/detail/bourns-inc/PTA6043-2015CPB103/3781230` |
| **Encoders** | 2 | Rotary Encoder w/ Push Button | `PEC11R-4215F-S0024` | `https://www.digikey.co.uk/en/products/detail/bourns-inc/PEC11R-4215F-S0024/4499665` |
| **Screens** | 5 | 0.91" OLED Display (I2C) | `Generic 128x32 SSD1306` | `https://www.aliexpress.com/item/1005008864162501.html` |
| **Multiplexer** | 1 | I2C Multiplexer (8-Channel) | `TCA9548A Breakout Board` | `https://www.aliexpress.com/item/1005010790267548.html` |

### Passive Components
| Component | Quantity | Value | Link |
| :--- | :--- | :--- | :--- |
| **Capacitors** | 5 | 0.1µF (100nF) | `https://www.digikey.co.uk/en/products/detail/vishay-beyschlag-draloric-bc-components/K104K10X7RF5UH5/2356754` |
| **Capacitor** | 1 | 100µF (25V) | `https://www.digikey.co.uk/en/products/detail/panasonic-electronic-components/ECA-1EM101B/268461` |

### Extra Components
| Component | Quantity | Link |
| :--- | :--- | :--- |
| **Female Headers** | 3 (80) | `https://www.digikey.co.uk/en/products/detail/sullins-connector-solutions/PRPC040SAAN-RC/2775214` |
| **Rotary Knobs** (Used to get rid of shipping) | 2 | `https://www.digikey.co.uk/en/products/detail/kilo-international/OEJL-90-4-5/710678` |


