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

## Firmware

[View README on firmware](Firmware/README.md)

## BOM

The complete list of hardware required to build this board.

| Part/Link | Manufacturer | Description | Qty | Price |
| :--- | :--- | :--- | :--- | :--- |
| **[PTA6043-2015CPB103](https://www.digikey.co.uk/en/products/detail/bourns-inc/PTA6043-2015CPB103/3781230)** | Bourns Inc. | SLIDE POT 10K OHM 0.25W TOP 60MM | 5 | £7.10 |
| **[K104K10X7RF5UH5](https://www.digikey.co.uk/en/products/detail/vishay-beyschlag-draloric-bc-components/K104K10X7RF5UH5/2356754)** | Vishay / BC Components | CAP CER 0.1UF 50V X7R RADIAL | 10 | £1.13 |
| **[ECA-1EM101B](https://www.digikey.co.uk/en/products/detail/panasonic-electronic-components/ECA-1EM101B/268461)** | Panasonic | CAP ALUM 100UF 20% 25V RADIAL TH | 2 | £0.46 |
| **[PEC11R-4215F-S0024](https://www.digikey.co.uk/en/products/detail/bourns-inc/PEC11R-4215F-S0024/4499665)** | Bourns Inc. | ENCODER MECH QUAD VERT PC PIN | 2 | £3.30 |
| **[OEJL-90-4-5](https://www.digikey.co.uk/en/products/detail/kilo-international/OEJL-90-4-5/710678)** | Kilo International | KNOB KNURLED 0.250" METAL | 2 | £18.68 |
| **[RNF14FTD10K0](https://www.digikey.co.uk/en/products/detail/stackpole-electronics-inc/RNF14FTD10K0/1706596)** | Stackpole Electronics Inc | RES 10K OHM 1% 1/4W AXIAL | 10 | £0.30 |
| **[1300-B](https://www.digikey.co.uk/en/products/detail/davies-molding-llc/1300-B/7908413)** | Davies Molding, LLC | KNOB KNURLED 0.236 X 0.118" NYL | 5 | £3.86 |
| **[MCP23017-E/SP](https://www.digikey.co.uk/en/products/detail/microchip-technology/MCP23017-E-SP/894272)** | Microchip Technology | IC XPNDR 1.7MHZ I2C 28SDIP | 2 | £2.54 |
| **[CFR-50JT-52-4K7](https://www.digikey.co.uk/en/products/detail/yageo/CFR-50JT-52-4K7/9099664)** | YAGEO | RES 4.7K OHM 5% 1/2W AXIAL | 10 | £0.34 |

Total Of Digikey: £45.37

| Part/Link | Description | Qty | Price |
| :--- | :--- | :--- | :--- |
| **[2.2" TFT LCD Module](https://www.aliexpress.com/item/1005008143782445.html)** | 2.2 TFT Full Color Screen LCD (Includes shipping) | 1 | £5.22 + £3.32 shipping |
| **[ESP32-S3-WROOM-1 N16R8](https://www.aliexpress.com/item/1005008796158734.html)** | ESP32 S3 Dev Board 44Pin Type-C 8M PSRAM | 1 | £5.28 |
| **Cherry Mx Switches** | Pre Owned Switches | 18 | £0.00 |

Estimated Total Of Aliexpress: £13.82 without discount

| Manufacturer Part Number | Manufacturer | Description | Qty | Price |
| :--- | :--- | :--- | :--- | :--- |
| **GerberFiles** | JLCPCB | PCB prototype: Black, 1.6 Thickness, HASL(with lead) | 5 | $13.10 |

Total Of JLCPCB: $21.08 or £15.80

For 3d Printing i will buy the filament which is about £10.25 from bambu labs.

**Grand Total: £85.24**

Libraries used:[
https://github.com/gorbachev/KiCad-SSD1306-0.91-OLED-4pin-128x32.pretty/tree/master](https://github.com/gorbachev/KiCad-SSD1306-0.91-OLED-4pin-128x32.pretty/tree/master)

[https://www.snapeda.com/parts/ESP32-DEVKITC-32E/Espressif%20Systems/view-part/?ref=search&t=esp32&ab_test_case=b](https://www.snapeda.com/parts/ESP32-DEVKITC-32E/Espressif%20Systems/view-part/?ref=search&t=esp32&ab_test_case=b)

[https://www.snapeda.com/parts/PEC12R-4217F-S0024/Bourns/view-part/?ref=search&t=rotary%20encoder](https://www.snapeda.com/parts/PEC12R-4217F-S0024/Bourns/view-part/?ref=search&t=rotary%20encoder)

[https://www.snapeda.com/parts/2717/Adafruit%20Industries/view-part/](https://www.snapeda.com/parts/2717/Adafruit%20Industries/view-part/)

[https://www.snapeda.com/parts/PTA4543-2015DPA103/Bourns/view-part/?ref=search&t=PTA4543-2015DPA103&ab_test_case=b](https://www.snapeda.com/parts/PTA4543-2015DPA103/Bourns/view-part/?ref=search&t=PTA4543-2015DPA103&ab_test_case=b)

[https://grabcad.com/library/0-91-oled-display-module-1/files?folder_id=13981557](https://grabcad.com/library/0-91-oled-display-module-1/files?folder_id=13981557)
