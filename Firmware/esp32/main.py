import time
import board
import analogio
import rotaryio
import keypad
import usb_cdc
import displayio
import terminalio
import microcontroller
from adafruit_display_text import label
from adafruit_ili9341 import ILI9341

TFT_CLK = board.IO18
TFT_MOSI = board.IO23
TFT_MISO = board.IO19
TFT_CS = board.IO15
TFT_DC = board.IO2
TFT_RST = board.IO4

FADER_PINS = (board.IO32, board.IO33, board.IO34, board.IO35, board.IO36)
ENCODER_ROTARY_PINS = ((board.IO25, board.IO26), (board.IO14, board.IO12))
ENCODER_SWITCH_PINS = (board.IO27, board.IO13)

COLOR_MASTER = 0xFFD700
COLOR_APP    = 0x00CED1
COLOR_MIC    = 0xFF4500
COLOR_OBS    = 0x9370DB
COLOR_MUTED  = 0x808080
COLOR_BG     = 0x000000

MODE_VOLUME = "VOLUME"
MODE_EQ = "EQ"
MODES = [MODE_VOLUME, MODE_EQ]

VOLUME_LABELS = ["MASTER", "APP 1", "APP 2", "MIC", "OBS"]
EQ_LABELS = ["80Hz", "320Hz", "1kHz", "3.2kHz", "10kHz"]
STRIP_COLORS = [COLOR_MASTER, COLOR_APP, COLOR_APP, COLOR_MIC, COLOR_OBS]


class ChannelStrip:
    def __init__(self, x, width, height, color):
        self.group = displayio.Group(x=x)
        self.width = width
        self.height = height
        self.color = color

        border = displayio.Bitmap(width - 4, height, 1)
        pal = displayio.Palette(2)
        pal[0] = COLOR_BG
        pal[1] = color
        self.group.append(displayio.TileGrid(border, pixel_shader=pal, x=2, y=0))

        self.name_label = label.Label(terminalio.FONT, text="---", color=0xFFFFFF, x=5, y=10)
        self.group.append(self.name_label)

        self.bar_bg = displayio.Bitmap(width - 20, height - 60, 2)
        bar_pal = displayio.Palette(3)
        bar_pal[0] = 0x222222
        bar_pal[1] = color
        bar_pal[2] = COLOR_MUTED
        bar_group = displayio.Group(x=10, y=30)
        bar_group.append(displayio.TileGrid(self.bar_bg, pixel_shader=bar_pal))
        self.group.append(bar_group)

        self.pct_label = label.Label(terminalio.FONT, text="0%", color=0xFFFFFF, x=15, y=height - 15)
        self.group.append(self.pct_label)

    def update(self, name, vol, muted=False):
        self.name_label.text = name[:8]
        self.pct_label.text = f"{vol}%"

        bar_h = self.bar_bg.height
        fill_h = int((vol / 100) * bar_h)

        self.bar_bg.fill(0)
        idx = 2 if muted else 1
        for y in range(bar_h - fill_h, bar_h):
            for x in range(self.bar_bg.width):
                self.bar_bg[x, y] = idx


class MixerFirmware:
    def __init__(self):
        self.mode = MODE_VOLUME
        self.labels = VOLUME_LABELS.copy()
        self.volumes = [0] * 5
        self.mutes = [False] * 5
        self.last_fader_vals = [-1] * 5
        self.last_enc_pos = [0, 0]

        self._init_display()
        self._init_faders()
        self._init_encoders()
        self._init_serial()

    def _init_display(self):
        displayio.release_displays()
        spi = board.SPI()
        bus = displayio.FourWire(spi, command=TFT_DC, chip_select=TFT_CS, reset=TFT_RST)
        self.display = ILI9341(bus, width=320, height=240, rotation=90)

        self.root = displayio.Group()
        self.display.show(self.root)

        bg = displayio.Bitmap(320, 240, 1)
        bg_pal = displayio.Palette(1)
        bg_pal[0] = COLOR_BG
        self.root.append(displayio.TileGrid(bg, pixel_shader=bg_pal))

        self.strips = []
        for i in range(5):
            strip = ChannelStrip(i * 64, 64, 240, STRIP_COLORS[i])
            self.strips.append(strip)
            self.root.append(strip.group)

    def _init_faders(self):
        self.faders = [analogio.AnalogIn(pin) for pin in FADER_PINS]
        self.fader_buf = [[0] * 10 for _ in range(5)]

    def _init_encoders(self):
        self.encoders = [
            rotaryio.IncrementalEncoder(a, b) for a, b in ENCODER_ROTARY_PINS
        ]
        self.keys = keypad.Keys(ENCODER_SWITCH_PINS, value_when_pressed=False, pull=True)

    def _init_serial(self):
        self.serial = usb_cdc.data if usb_cdc.data else usb_cdc.console

    def smooth_fader(self, i):
        val = self.faders[i].value
        buf = self.fader_buf[i]
        buf.pop(0)
        buf.append(val)
        return sum(buf) // len(buf)

    def send(self, msg):
        if self.serial:
            try:
                self.serial.write(f"{msg}\n".encode("utf-8"))
            except Exception:
                pass

    def read_serial(self):
        if not self.serial or not self.serial.in_waiting:
            return
        try:
            line = self.serial.readline().decode("utf-8").strip()
            if line:
                self.handle_command(line)
        except Exception:
            pass

    def handle_command(self, line):
        parts = line.split(":")
        if not parts:
            return
        cmd = parts[0]

        if cmd == "APP" and len(parts) >= 4:
            try:
                ch = int(parts[1])
                name = parts[3] if parts[3] else self.labels[ch]
                vol = int(parts[4]) if len(parts) > 4 else self.volumes[ch]
                if 0 <= ch < 5:
                    self.labels[ch] = name
                    self.volumes[ch] = vol
                    self.strips[ch].update(name, vol, self.mutes[ch])
            except (ValueError, IndexError):
                pass

        elif cmd == "PING":
            self.send("PONG")

        elif cmd == "MODE" and len(parts) >= 2:
            new_mode = parts[1]
            if new_mode in MODES and new_mode != self.mode:
                self.mode = new_mode
                microcontroller.reset()

    def run(self):
        if self.mode == MODE_VOLUME:
            self.labels = VOLUME_LABELS.copy()
        else:
            self.labels = EQ_LABELS.copy()

        for i in range(5):
            self.strips[i].update(self.labels[i], self.volumes[i], self.mutes[i])

        while True:
            self.read_serial()

            for i in range(5):
                raw = self.smooth_fader(i)
                vol = int((raw / 65535) * 100)
                if abs(vol - self.last_fader_vals[i]) > 1:
                    self.last_fader_vals[i] = vol
                    self.volumes[i] = vol
                    self.send(f"VOL:{i}:{vol}")
                    self.strips[i].update(self.labels[i], vol, self.mutes[i])

            for i, enc in enumerate(self.encoders):
                pos = enc.position
                delta = pos - self.last_enc_pos[i]
                if delta != 0:
                    self.send(f"SELECT:{1 + i}:{1 if delta > 0 else -1}")
                    self.last_enc_pos[i] = pos

            event = self.keys.events.get()
            if event and event.pressed:
                if event.key_number == 0:
                    self.mode = MODE_EQ if self.mode == MODE_VOLUME else MODE_VOLUME
                    self.send(f"MODE:{self.mode}")
                    microcontroller.reset()
                elif event.key_number == 1:
                    self.mutes[0] = not self.mutes[0]
                    self.send(f"MUT:0:{int(self.mutes[0])}")
                    self.strips[0].update(self.labels[0], self.volumes[0], self.mutes[0])

            time.sleep(0.01)


if __name__ == "__main__":
    MixerFirmware().run()
