# Custom Mixer ESP32 (v2.0)

This project uses an ESP32 to read 5 linear faders, 2 rotary encoders, and 18 switches, with programmable buttons acting like MIDI and everything that happens, as a change in volume will show on the 2.2-inch screen.

This project's purpose is to act as a mixer and control the volume of an app when it sounds too loud or too quiet.

The Rotary Encoders will be used as a selector to scroll through active apps and the slider they should be on, or potentially as a master volume control.

## Schematic

<img width="3507" height="2480" alt="image" src="https://github.com/user-attachments/assets/fe5eb330-c6c7-4392-acde-6153008f6953" />

## PCB

<img width="2339" height="1654" alt="aab3a241-1" src="https://github.com/user-attachments/assets/b921ea87-ec00-4a68-93e3-a655f242e24a" />
<img width="2339" height="1654" alt="aab3a241-2" src="https://github.com/user-attachments/assets/7a1b743c-059d-4339-8dbb-09326ecc156f" />

## CAD

<img width="936" height="640" alt="image" src="https://github.com/user-attachments/assets/373d0f83-c83b-462d-b2b2-12c4fb762086" />

<img width="1197" height="766" alt="image" src="https://github.com/user-attachments/assets/0e115ebd-ca7c-4ac0-829d-5940272769e9" />

## Quick Start

### 1. Flash the ESP32-S3 Firmware

1. Install [CircuitPython 9.x](https://circuitpython.org/board/espressif_esp32s3_devkitc_1_n8r8/) on your ESP32-S3
2. Copy `Firmware/esp32/main.py` and `Firmware/esp32/boot.py` to the **CIRCUITPY** drive
3. Copy these libraries to the `/lib` folder on the drive (from the [CircuitPython Bundle](https://circuitpython.org/libraries)):
   - `adafruit_ili9341.mpy`
   - `adafruit_display_text/`
   - `adafruit_bus_device/`

### 2. Run the PC Software

```bash
pip install pycaw pyserial pystray psutil Pillow pywin32 obs-websocket-py
python Firmware/mixer.py --console
```

Run `python Firmware/mixer.py --help` for all options (COM port override, test mode, etc.).

> Requires **Windows 10/11**, **Python 3.10+**, and optionally **EqualizerAPO** (for EQ mode) and **OBS with WebSocket** (for OBS channel).

## Firmware

[View detailed firmware documentation](Firmware/README.md)

## BOM

The complete list of hardware required to build this project.

### Digikey

| Part | Description | Qty | Price |
| :--- | :--- | :--- | :--- |
| **[PTA6043-2015CPB103](https://www.digikey.co.uk/en/products/detail/bourns-inc/PTA6043-2015CPB103/3781230)** | Bourns — Slide Pot 10K, 60mm | 5 | £7.10 |
| **[K104K10X7RF5UH5](https://www.digikey.co.uk/en/products/detail/vishay-beyschlag-draloric-bc-components/K104K10X7RF5UH5/2356754)** | Vishay — Ceramic Cap 0.1µF 50V | 10 | £1.13 |
| **[ECA-1EM101B](https://www.digikey.co.uk/en/products/detail/panasonic-electronic-components/ECA-1EM101B/268461)** | Panasonic — Electrolytic Cap 100µF 25V | 2 | £0.46 |
| **[PEC11R-4215F-S0024](https://www.digikey.co.uk/en/products/detail/bourns-inc/PEC11R-4215F-S0024/4499665)** | Bourns — Rotary Encoder | 2 | £3.30 |
| **[PRPC040SAAN-RC](https://www.digikey.co.uk/en/products/detail/sullins-connector-solutions/PRPC040SAAN-RC/2775214)** | Sullins — 40-Pin Header | 3 | £1.23 |
| **[RNF14FTD10K0](https://www.digikey.co.uk/en/products/detail/stackpole-electronics-inc/RNF14FTD10K0/1706596)** | Stackpole — 10K Resistor 1/4W | 10 | £0.30 |
| **[CFR-50JT-52-4K7](https://www.digikey.co.uk/en/products/detail/yageo/CFR-50JT-52-4K7/9099664)** | YAGEO — 4.7K Resistor 1/2W | 10 | £0.34 |
| **[OEJL-90-4-5](https://www.digikey.co.uk/en/products/detail/kilo-international/OEJL-90-4-5/710678)** | Kilo International — Solid Aluminium Knob | 2 | £18.68 |
| **[1300-B](https://www.digikey.co.uk/en/products/detail/davies-molding-llc/1300-B/7908413)** | Davies Molding — Nylon Knob | 5 | £3.86 |
| **[MCP23017-E/SP](https://www.digikey.co.uk/en/products/detail/microchip-technology/MCP23017-E-SP/894272)** | Microchip — I²C I/O Expander 28-SDIP | 2 | £2.54 |

Digikey Total: £45.37

### AliExpress

| Part | Description | Qty | Price |
| :--- | :--- | :--- | :--- |
| **[2.2" TFT LCD](https://www.aliexpress.com/item/1005008143782445.html)** | 2.2" ILI9341 Full Color TFT (includes shipping) | 1 | £5.22 + £3.32 shipping |
| **[ESP32-S3-WROOM-1 N16R8](https://www.aliexpress.com/item/1005008796158734.html)** | ESP32-S3 Dev Board, 44-Pin, 8M PSRAM | 1 | £5.28 |
| **Cherry MX Switches** | Pre-owned mechanical switches | 18 | £0.00 |

Estimated AliExpress Total: £13.82 without discount

### Manufacturing

| Part | Description | Qty | Price |
| :--- | :--- | :--- | :--- |
| **[JLCPCB PCB](https://jlcpcb.com/)** | PCB prototype (black, 1.6mm, HASL with lead) | 5 | $13.10 |

JLCPCB Total: $21.08 or £15.80

For 3D printing, filament is about £10.25 from Bambu Labs.

**Grand Total: £85.24**

## KiCad Libraries

- [SSD1306 OLED Footprint](https://github.com/gorbachev/KiCad-SSD1306-0.91-OLED-4pin-128x32.pretty/tree/master)
- [ESP32-DEVKITC-32E](https://www.snapeda.com/parts/ESP32-DEVKITC-32E/Espressif%20Systems/view-part/?ref=search&t=esp32&ab_test_case=b)
- [PEC12R Rotary Encoder](https://www.snapeda.com/parts/PEC12R-4217F-S0024/Bourns/view-part/?ref=search&t=rotary%20encoder)
- [Adafruit 2717](https://www.snapeda.com/parts/2717/Adafruit%20Industries/view-part/)
- [PTA4543 Slide Pot](https://www.snapeda.com/parts/PTA4543-2015DPA103/Bourns/view-part/?ref=search&t=PTA4543-2015DPA103&ab_test_case=b)
- [0.91" OLED 3D Model](https://grabcad.com/library/0-91-oled-display-module-1/files?folder_id=13981557)
