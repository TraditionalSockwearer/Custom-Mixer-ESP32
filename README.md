# Custom Mixer ESP32 (v1.0)

This project uses an ESP32 to read 5 linear faders and 2 rotary encoders, displaying real-time volume levels for specific apps, chosen via the rotary encoder, on individual OLED screens.

This project's purpose is to act as a mixer and control the volume of an app when it sounds too loud or too quiet.

The Rotary Encoders will be used as a selecter to scroll through the apps that are active and which slider it should be on.

## Schematic
<img width="3507" height="2480" alt="image" src="https://github.com/user-attachments/assets/8e63d87b-bb34-4a7e-8cb1-daa19f77bfc7" />

## PCB
<img width="2339" height="1654" alt="Custom-Mixer-ESP32__Assembly-2" src="https://github.com/user-attachments/assets/c7fb8ef5-2a20-432a-8b57-7e638c903e34" />
<img width="2339" height="1654" alt="Custom-Mixer-ESP32__Assembly-1" src="https://github.com/user-attachments/assets/863af401-8091-4f20-94fa-95c099853398" />


## CAD

<img width="933" height="673" alt="image" src="https://github.com/user-attachments/assets/9b5bbf24-a97c-4869-9bb0-e8a22925a90a" />

<img width="1332" height="699" alt="image" src="https://github.com/user-attachments/assets/dbe583d6-05be-4020-9771-ea5ec2be287e" />


## BOM

The complete list of hardware required to build this board.
### Core Electronics
| Component | Quantity | Description | Part Number| Link |
| :--- | :--- | :--- | :--- | :--- |
| **Microcontroller** | 1 | ESP32-DevKitC V4 | `ESP32-DEVKITC-32E` | [https://www.digikey.co.uk/en/products/detail/espressif-systems/ESP32-DEVKITC-32E/12091810](https://www.digikey.co.uk/en/products/detail/espressif-systems/ESP32-DEVKITC-32E/12091810) |
| **Faders** | 5 | 60mm Slide Potentiometer | `Bourns PTA6043-2015CPB103` | [https://www.digikey.co.uk/en/products/detail/bourns-inc/PTA6043-2015CPB103/3781230](https://www.digikey.co.uk/en/products/detail/bourns-inc/PTA6043-2015CPB103/3781230) |
| **Encoders** | 2 | Rotary Encoder w/ Push Button | `PEC11R-4215F-S0024` | [https://www.digikey.co.uk/en/products/detail/bourns-inc/PEC11R-4215F-S0024/4499665](https://www.digikey.co.uk/en/products/detail/bourns-inc/PEC11R-4215F-S0024/4499665) |
| **Screens** | 5 | 0.91" OLED Display (I2C) | `Generic 128x32 SSD1306` | [https://www.aliexpress.com/item/1005008864162501.html](https://www.aliexpress.com/item/1005008864162501.html) |
| **Multiplexer** | 1 | I2C Multiplexer (8-Channel) | `TCA9548A Breakout Board` | [https://www.aliexpress.com/item/1005010790267548.html](https://www.aliexpress.com/item/1005010790267548.html) |

### Passive Components
| Component | Quantity | Value | Link |
| :--- | :--- | :--- | :--- |
| **Capacitors** | 5 | 0.1µF (100nF) | [https://www.digikey.co.uk/en/products/detail/vishay-beyschlag-draloric-bc-components/K104K10X7RF5UH5/2356754](https://www.digikey.co.uk/en/products/detail/vishay-beyschlag-draloric-bc-components/K104K10X7RF5UH5/2356754) |
| **Capacitor** | 1 | 100µF (25V) | [https://www.digikey.co.uk/en/products/detail/panasonic-electronic-components/ECA-1EM101B/268461](https://www.digikey.co.uk/en/products/detail/panasonic-electronic-components/ECA-1EM101B/268461) |

### Extra Components
| Component | Quantity | Link |
| :--- | :--- | :--- |
| **Female Headers** | 3 (80) | [https://www.digikey.co.uk/en/products/detail/sullins-connector-solutions/PRPC040SAAN-RC/2775214](https://www.digikey.co.uk/en/products/detail/sullins-connector-solutions/PRPC040SAAN-RC/2775214) |
| **Rotary Knobs** (Used to get rid of shipping) | 2 | [https://www.digikey.co.uk/en/products/detail/kilo-international/OEJL-90-4-5/710678](https://www.digikey.co.uk/en/products/detail/kilo-international/OEJL-90-4-5/710678) |
| **Paper Clip** | 2

Libraries used:[
https://github.com/gorbachev/KiCad-SSD1306-0.91-OLED-4pin-128x32.pretty/tree/master](https://github.com/gorbachev/KiCad-SSD1306-0.91-OLED-4pin-128x32.pretty/tree/master)

[https://www.snapeda.com/parts/ESP32-DEVKITC-32E/Espressif%20Systems/view-part/?ref=search&t=esp32&ab_test_case=b](https://www.snapeda.com/parts/ESP32-DEVKITC-32E/Espressif%20Systems/view-part/?ref=search&t=esp32&ab_test_case=b)

[https://www.snapeda.com/parts/PEC12R-4217F-S0024/Bourns/view-part/?ref=search&t=rotary%20encoder](https://www.snapeda.com/parts/PEC12R-4217F-S0024/Bourns/view-part/?ref=search&t=rotary%20encoder)

[https://www.snapeda.com/parts/2717/Adafruit%20Industries/view-part/](https://www.snapeda.com/parts/2717/Adafruit%20Industries/view-part/)

[https://www.snapeda.com/parts/PTA4543-2015DPA103/Bourns/view-part/?ref=search&t=PTA4543-2015DPA103&ab_test_case=b](https://www.snapeda.com/parts/PTA4543-2015DPA103/Bourns/view-part/?ref=search&t=PTA4543-2015DPA103&ab_test_case=b)

[https://grabcad.com/library/0-91-oled-display-module-1/files?folder_id=13981557](https://grabcad.com/library/0-91-oled-display-module-1/files?folder_id=13981557)
