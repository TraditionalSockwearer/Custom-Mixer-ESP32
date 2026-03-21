# ESP32-S3 Mixer Firmware

CircuitPython firmware for the Custom Mixer running on an ESP32-S3 with a 2.2" TFT display.

## Hardware

- ESP32-S3 devboard
- 2.2" ILI9341 SPI TFT (320x240, full color)
- 5x Linear faders (analog)
- 2x Rotary encoders with push buttons

### Wiring

| Component | Pin   |
|-----------|-------|
| TFT SCK   | IO18  |
| TFT MOSI  | IO23  |
| TFT MISO  | IO19  |
| TFT CS    | IO15  |
| TFT DC    | IO2   |
| TFT RST   | IO4   |
| Fader 1   | IO32  |
| Fader 2   | IO33  |
| Fader 3   | IO34  |
| Fader 4   | IO35  |
| Fader 5   | IO36  |
| Enc 1 A/B | IO25/IO26 |
| Enc 2 A/B | IO14/IO12 |
| Enc 1 Btn | IO27  |
| Enc 2 Btn | IO13  |

## Modes

### Volume Mixer
- 5 channel strips on one screen: Master, App 1, App 2, Mic, OBS
- Faders control per-channel volume
- Encoders cycle which app is assigned to channels 2 and 3
- Button 1 toggles between Volume and EQ mode
- Button 2 mutes the Master channel

### EQ Control
- Faders map to 5-band EQ: 80Hz, 320Hz, 1kHz, 3.2kHz, 10kHz
- Range: -15dB to +15dB
- Requires EqualizerAPO on the PC

## Installation

1. Install CircuitPython on your ESP32-S3
2. Copy `main.py` and `boot.py` to the CIRCUITPY drive
3. Copy these libraries to `/lib`:
   - `adafruit_ili9341.mpy`
   - `adafruit_display_text/`
   - `adafruit_bus_device/`

## Serial Protocol

USB CDC at 115200 baud.

### PC → ESP32
```
APP:<ch>:<icon>:<name>:<vol>    Channel info
APPS:<count>                    Channel count
MODE:<mode>                     Switch mode
PING                            Keepalive
```

### ESP32 → PC
```
VOL:<ch>:<vol>                  Fader value (0-100)
SELECT:<ch>:<dir>               Encoder rotation
MODE:<mode>                     Mode change request
MUT:<ch>:<state>                Mute toggle
PONG                            Keepalive response
```
