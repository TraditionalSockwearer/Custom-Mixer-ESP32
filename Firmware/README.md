# Custom Mixer

Companion software and firmware for a custom digital mixer built around an ESP32-S3.

## Overview

5 faders, 2 rotary encoders, and a 2.2" color TFT on an ESP32-S3. Controls system audio, per-app volume, microphone input, OBS, and headphone EQ from one device.

## Structure

```
mixer.py              ← single PC script (run this)
Firmware/esp32/       ← CircuitPython firmware for ESP32-S3
```

### Channel Layout

| Fader | Control |
|-------|---------|
| 1 | Master Volume |
| 2 | App 1 (cycle with encoder) |
| 3 | App 2 (cycle with encoder) |
| 4 | Microphone Input |
| 5 | OBS Desktop Audio |

### EQ Mode

Button 1 toggles EQ mode — faders map to 80Hz, 320Hz, 1kHz, 3.2kHz, 10kHz via EqualizerAPO.

## Usage

```bash
pip install pycaw pyserial pystray psutil Pillow pywin32 obs-websocket-py
python mixer.py --console
```

### Options
```
--port, -p    COM port (auto-detected if omitted)
--console, -c Run without system tray
--test, -t    Print audio sessions and exit
```

## Requirements
- Python 3.10+
- Windows 10/11
- EqualizerAPO (for EQ mode)
- OBS with WebSocket enabled (for OBS channel)

