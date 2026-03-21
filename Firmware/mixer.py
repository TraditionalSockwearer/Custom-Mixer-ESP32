import os
import io
import time
import threading
import argparse
from typing import Optional, Dict, List, Callable, Set
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import serial
import serial.tools.list_ports
from ctypes import POINTER, cast
import comtypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import psutil

try:
    from pycaw.pycaw import IAudioEndpointVolume
except ImportError:
    IAudioEndpointVolume = None

try:
    from obswebsocket import obsws, requests as obs_requests
    HAS_OBS = True
except ImportError:
    HAS_OBS = False

try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False

try:
    import win32gui
    import win32ui
    HAS_PYWIN32 = True
except ImportError:
    HAS_PYWIN32 = False

try:
    comtypes.CoInitialize()
except OSError:
    pass


# ── Data ─────────────────────────────────────────────────────────────────────

@dataclass
class AudioSession:
    process_id: int
    process_name: str
    display_name: str
    volume: float
    is_muted: bool
    def __hash__(self):
        return hash(self.process_id)

@dataclass
class EQBand:
    name: str
    frequency: int
    gain: float
    q: float


# ── Audio Controller ─────────────────────────────────────────────────────────

class AudioController:
    DISPLAY_NAMES = {
        'chrome.exe': 'Chrome', 'firefox.exe': 'Firefox', 'msedge.exe': 'Edge',
        'discord.exe': 'Discord', 'spotify.exe': 'Spotify', 'steam.exe': 'Steam',
        'vlc.exe': 'VLC', 'obs64.exe': 'OBS', 'explorer.exe': 'System',
        'audiodg.exe': 'System Audio', 'signalrgb.exe': 'SignalRGB',
        'signalrgbcore.exe': 'SignalRGB',
    }
    BLOCKED_APPS = {
        'grammarly.exe', 'grammarlydesktop.exe', 'grammarly.desktop.exe',
        'antivirus', 'avgui.exe', 'avast', 'norton', 'mcafee',
        'searchhost.exe', 'searchapp.exe', 'runtimebroker.exe',
        'backgroundtaskhost.exe', 'shellexperiencehost.exe',
        'startmenuexperiencehost.exe', 'lockapp.exe', 'textinputhost.exe',
    }

    def __init__(self):
        self._master_volume = None
        self._input_volume = None
        self._callbacks: List[Callable] = []
        self._monitor_thread: Optional[threading.Thread] = None
        self._running = False
        self._init_master()
        self._init_input()

    def _init_master(self):
        try:
            devices = AudioUtilities.GetSpeakers()
            if hasattr(devices, 'EndpointVolume'):
                self._master_volume = devices.EndpointVolume
                return
            if hasattr(devices, '_volume'):
                self._master_volume = devices._volume
                return
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self._master_volume = cast(interface, POINTER(IAudioEndpointVolume))
        except Exception:
            pass

    def _init_input(self):
        try:
            mic = AudioUtilities.GetMicrophone()
            if not mic:
                return
            interface = mic.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self._input_volume = cast(interface, POINTER(IAudioEndpointVolume))
        except Exception:
            pass

    def get_sessions(self):
        sessions = []
        seen = set()
        try:
            for s in AudioUtilities.GetAllSessions():
                if s.Process is None:
                    continue
                try:
                    name = s.Process.name()
                    lower = name.lower()
                    if lower in seen or lower in self.BLOCKED_APPS:
                        continue
                    vol = s._ctl.QueryInterface(ISimpleAudioVolume)
                    sessions.append(AudioSession(
                        process_id=s.Process.pid, process_name=name,
                        display_name=self._display_name(name),
                        volume=vol.GetMasterVolume(), is_muted=vol.GetMute()
                    ))
                    seen.add(lower)
                except Exception:
                    continue
        except Exception:
            pass
        return sessions

    def _display_name(self, name):
        lower = name.lower()
        return self.DISPLAY_NAMES.get(lower, name.replace('.exe', '').capitalize())

    def set_session_volume(self, process_name, volume):
        try:
            comtypes.CoInitialize()
        except:
            pass
        volume = max(0.0, min(1.0, volume))
        try:
            target = process_name.lower()
            for s in AudioUtilities.GetAllSessions():
                try:
                    if s.Process and s.Process.name().lower() == target:
                        s._ctl.QueryInterface(ISimpleAudioVolume).SetMasterVolume(volume, None)
                        return True
                except Exception:
                    continue
        except Exception:
            pass
        return False

    def get_master_volume(self):
        if self._master_volume:
            try:
                if hasattr(self._master_volume, 'level'):
                    return self._master_volume.level
                return self._master_volume.GetMasterVolumeLevelScalar()
            except Exception:
                pass
        return 0.0

    def set_master_volume(self, volume):
        volume = max(0.0, min(1.0, volume))
        if self._master_volume:
            try:
                if hasattr(self._master_volume, 'level'):
                    self._master_volume.level = volume
                    return True
                self._master_volume.SetMasterVolumeLevelScalar(volume, None)
                return True
            except Exception:
                pass
        return False

    def get_input_volume(self):
        ctrl = self._input_volume
        if ctrl:
            try:
                return ctrl.GetMasterVolumeLevelScalar()
            except Exception:
                pass
        return 0.0

    def set_input_volume(self, volume):
        volume = max(0.0, min(1.0, volume))
        ctrl = self._input_volume
        if ctrl:
            try:
                ctrl.SetMasterVolumeLevelScalar(volume, None)
                return True
            except Exception:
                pass
        return False

    def register_session_callback(self, callback):
        self._callbacks.append(callback)

    def start_monitoring(self, interval=1.0):
        if self._monitor_thread and self._monitor_thread.is_alive():
            return
        self._running = True
        self._monitor_thread = threading.Thread(target=self._monitor, args=(interval,), daemon=True)
        self._monitor_thread.start()

    def stop_monitoring(self):
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)

    def _monitor(self, interval):
        try:
            comtypes.CoInitialize()
        except:
            pass
        last_ids = set()
        while self._running:
            sessions = self.get_sessions()
            ids = {s.process_id for s in sessions}
            if ids != last_ids:
                last_ids = ids
                for cb in self._callbacks:
                    try:
                        cb(sessions)
                    except Exception:
                        pass
            time.sleep(interval)


# ── OBS Controller ───────────────────────────────────────────────────────────

class OBSController:
    def __init__(self, host="localhost", port=4455, password=""):
        self.host = host
        self.port = port
        self.password = password
        self.ws = None
        self._connected = False

    def connect(self):
        if not HAS_OBS:
            return False
        try:
            self.ws = obsws(self.host, self.port, self.password)
            self.ws.connect()
            self._connected = True
            return True
        except Exception:
            return False

    def set_volume(self, source, volume):
        if not self._connected:
            return
        try:
            self.ws.call(obs_requests.SetInputVolume(inputName=source, inputVolumeMul=volume))
        except Exception:
            pass

    def get_volume(self, source):
        if not self._connected:
            return 0.0
        try:
            return self.ws.call(obs_requests.GetInputVolume(inputName=source)).getInputVolumeMul()
        except Exception:
            return 0.0

    def disconnect(self):
        if self.ws:
            self.ws.disconnect()
            self._connected = False


# ── Equalizer APO ────────────────────────────────────────────────────────────

class EqualizerAPO:
    APO_PATHS = [
        Path(os.environ.get('ProgramFiles', 'C:\\Program Files')) / "EqualizerAPO",
        Path(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')) / "EqualizerAPO",
    ]
    DEFAULT_BANDS = [
        EQBand("Low", 80, 0.0, 0.7), EQBand("Low-Mid", 320, 0.0, 0.7),
        EQBand("Mid", 1000, 0.0, 0.7), EQBand("High-Mid", 3200, 0.0, 0.7),
        EQBand("High", 10000, 0.0, 0.7),
    ]

    def __init__(self):
        self.apo_path: Optional[Path] = None
        self.config_path: Optional[Path] = None
        self.bands = [EQBand(b.name, b.frequency, b.gain, b.q) for b in self.DEFAULT_BANDS]
        for p in self.APO_PATHS:
            if p.exists():
                self.apo_path = p
                self.config_path = p / "config"
                break

    @property
    def is_installed(self):
        return self.apo_path is not None and self.apo_path.exists()

    def initialize(self):
        if not self.is_installed:
            return False
        if not self._write_config():
            return False
        self._ensure_included()
        return True

    def set_band_gain(self, index, gain):
        if index < 0 or index >= len(self.bands):
            return False
        self.bands[index].gain = max(-15.0, min(15.0, gain))
        return self._write_config()

    def _write_config(self):
        if not self.config_path:
            return False
        try:
            lines = ["Preamp: 0 dB", ""]
            for b in self.bands:
                lines.append(f"Filter: ON PK Fc {b.frequency} Hz Gain {b.gain:.1f} dB Q {b.q}")
            (self.config_path / "mixer_eq.txt").write_text('\n'.join(lines), encoding='utf-8')
            return True
        except Exception:
            return False

    def _ensure_included(self):
        if not self.config_path:
            return
        main = self.config_path / "config.txt"
        if not main.exists():
            return
        try:
            content = main.read_text(encoding='utf-8')
            if "mixer_eq.txt" not in content:
                with main.open('a', encoding='utf-8') as f:
                    f.write("\nInclude: mixer_eq.txt\n")
        except Exception:
            pass


# ── Icon Extractor ───────────────────────────────────────────────────────────

_MST_ICON = bytes([
    0x00, 0x00, 0x01, 0x80, 0x03, 0xC0, 0x07, 0xE0,
    0x0F, 0xF0, 0x0F, 0xF0, 0x0F, 0xF0, 0x0F, 0xF0,
    0x0F, 0xF0, 0x0F, 0xF0, 0x0F, 0xF0, 0x0F, 0xF0,
    0x07, 0xE0, 0x03, 0xC0, 0x01, 0x80, 0x00, 0x00
])
_APP_ICON = bytes([
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFC,
    0x40, 0x02, 0x40, 0x02, 0x40, 0x02, 0x40, 0x02,
    0x40, 0x02, 0x40, 0x02, 0x40, 0x02, 0x40, 0x02,
    0x3F, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
])

class IconExtractor:
    def __init__(self, cache_dir="icon_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self._cache = {"mst": _MST_ICON, "app": _APP_ICON}

    def get_icon(self, process_name, is_master=False):
        if is_master:
            return self._cache["mst"]
        if not process_name:
            return self._cache["app"]
        if process_name in self._cache:
            return self._cache[process_name]

        path = os.path.join(self.cache_dir, f"{process_name}.bin")
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = f.read()
            self._cache[process_name] = data
            return data

        data = self._extract(process_name)
        if data:
            with open(path, "wb") as f:
                f.write(data)
            self._cache[process_name] = data
            return data
        return self._cache["app"]

    def _extract(self, process_name):
        if not HAS_PYWIN32:
            return None
        try:
            from PIL import Image
            exe = None
            for proc in psutil.process_iter(['name', 'exe']):
                if proc.info['name'].lower() == process_name.lower():
                    exe = proc.info['exe']
                    break
            if not exe:
                return None

            large, small = win32gui.ExtractIconEx(exe, 0)
            if not small and not large:
                return None
            h = small[0] if small else large[0]
            for x in large + small:
                if x != h:
                    win32gui.DestroyIcon(x)

            info = win32gui.GetIconInfo(h)
            bmp = win32gui.GetObject(info[4])
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            mem = hdc.CreateCompatibleDC()
            old = mem.SelectObject(win32ui.CreateBitmapFromHandle(info[4]))
            bits = mem.GetSafeHdc().GetBitmapBits(True)
            img = Image.frombuffer('RGBA', (bmp.bmWidth, bmp.bmHeight), bits, 'raw', 'BGRA', 0, 1)
            mem.SelectObject(old)
            mem.DeleteDC()
            hdc.DeleteDC()
            win32gui.DestroyIcon(h)

            img = img.resize((16, 16), Image.Resampling.LANCZOS).convert("L")
            img = img.point(lambda p: 1 if p > 127 else 0, mode='1')
            return img.tobytes()
        except Exception:
            return None


# ── Serial Protocol ──────────────────────────────────────────────────────────

class MessageType(Enum):
    APP_INFO = "APP"
    APP_COUNT = "APPS"
    ICON = "ICON"
    VOLUME = "VOL"
    SELECT = "SELECT"
    MODE = "MODE"
    PING = "PING"
    PONG = "PONG"

class SerialProtocol:
    BAUD_RATE = 115200

    def __init__(self, port=None):
        self.port = port
        self.serial: Optional[serial.Serial] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._callbacks: Dict[MessageType, List[Callable]] = {t: [] for t in MessageType}
        self._lock = threading.Lock()

    def find_port(self):
        ports = list(serial.tools.list_ports.comports())
        cp = [p for p in ports if 'circuitpython' in p.description.lower() or p.vid == 0x2886]
        if len(cp) >= 2:
            cp.sort(key=lambda p: int(p.device.replace('COM', '')))
            return cp[-1].device
        if cp:
            return cp[0].device
        for p in ports:
            desc = p.description.lower()
            if any(x in desc for x in ['cp210', 'ch340', 'esp32', 'usb serial']):
                return p.device
            if p.vid in [0x10C4, 0x1A86]:
                return p.device
        return None

    def connect(self, port=None):
        if port:
            self.port = port
        elif not self.port:
            self.port = self.find_port()
        if not self.port:
            return False
        try:
            self.serial = serial.Serial(self.port, self.BAUD_RATE, timeout=0.1)
            self._running = True
            self._thread = threading.Thread(target=self._read_loop, daemon=True)
            self._thread.start()
            return True
        except serial.SerialException:
            return False

    def disconnect(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        if self.serial:
            self.serial.close()
            self.serial = None

    def is_connected(self):
        return self.serial is not None and self.serial.is_open

    def register_callback(self, msg_type, callback):
        self._callbacks[msg_type].append(callback)

    def send_app_info(self, ch, icon, name, vol):
        self._send(f"APP:{ch}:{icon}:{name}:{vol}")

    def send_app_count(self, count):
        self._send(f"APPS:{count}")

    def send_icon(self, ch, data):
        self._send(f"ICON:{ch}:{data.hex()}")

    def send_ping(self):
        self._send("PING")

    def _send(self, msg):
        if self.serial and self.serial.is_open:
            with self._lock:
                try:
                    self.serial.write(f"{msg}\n".encode('utf-8'))
                except serial.SerialException:
                    pass

    def _read_loop(self):
        while self._running and self.serial:
            try:
                if self.serial.in_waiting:
                    line = self.serial.readline().decode('utf-8').strip()
                    if line:
                        self._parse(line)
            except serial.SerialException:
                break
            except UnicodeDecodeError:
                continue
            time.sleep(0.01)

    def _parse(self, line):
        parts = line.split(':')
        if not parts:
            return
        try:
            mt = MessageType(parts[0])
            for cb in self._callbacks[mt]:
                cb(parts[1:] if len(parts) > 1 else [])
        except ValueError:
            pass


# ── Channel Manager ──────────────────────────────────────────────────────────

@dataclass
class Channel:
    index: int
    is_master: bool = False
    assigned_session: Optional[AudioSession] = None
    volume: float = 1.0

    @property
    def display_name(self):
        if self.is_master:
            return "MASTER"
        s = self.assigned_session
        return s.display_name if s else f"CH{self.index}"

    @property
    def process_name(self):
        s = self.assigned_session
        return s.process_name if s else None

LAYOUT = ["MASTER", "APP", "APP", "INPUT", "OBS"]
APP_INDICES = [1, 2]
ICON_MAP = {
    "chrome.exe": "CHR", "discord.exe": "DIS", "spotify.exe": "SPT",
    "steam.exe": "STM", "obs64.exe": "OBS", "obs.exe": "OBS",
    "firefox.exe": "FFX", "msedge.exe": "EDG",
}

class ChannelManager:
    def __init__(self, audio, obs):
        self.audio = audio
        self.obs = obs
        self.channels: List[Channel] = []
        self._callbacks: List[Callable] = []
        self.audio.register_session_callback(self._on_sessions_changed)

    def initialize(self):
        self._rebuild()

    def _rebuild(self):
        sessions = self.audio.get_sessions()
        self.channels = []
        for i, t in enumerate(LAYOUT):
            ch = Channel(index=i)
            if t == "MASTER":
                ch.is_master = True
                ch.volume = self.audio.get_master_volume()
            elif t == "INPUT":
                ch.volume = self.audio.get_input_volume()
            elif t == "APP":
                used = [c.assigned_session for c in self.channels if c.assigned_session]
                for s in sessions:
                    if s not in used:
                        ch.assigned_session = s
                        ch.volume = s.volume
                        break
            self.channels.append(ch)
        self._notify_all()

    def _on_sessions_changed(self, sessions):
        for i in APP_INDICES:
            ch = self.channels[i]
            if ch.assigned_session:
                match = next((s for s in sessions if s.process_name == ch.assigned_session.process_name), None)
                if match:
                    ch.assigned_session = match
                    ch.volume = match.volume
                else:
                    ch.assigned_session = None
            if ch.assigned_session is None:
                used = [c.assigned_session for c in self.channels if c.assigned_session]
                for s in sessions:
                    if s not in used:
                        ch.assigned_session = s
                        ch.volume = s.volume
                        break
        self._notify_all()

    def set_volume(self, index, volume):
        if index < 0 or index >= len(self.channels):
            return False
        ch = self.channels[index]
        ch.volume = volume
        t = LAYOUT[index]
        if t == "MASTER":
            return self.audio.set_master_volume(volume)
        elif t == "INPUT":
            return self.audio.set_input_volume(volume)
        elif t == "APP" and ch.assigned_session:
            return self.audio.set_session_volume(ch.assigned_session.process_name, volume)
        elif t == "OBS":
            self.obs.set_volume("Desktop Audio", volume)
            return True
        return False

    def cycle_app(self, index, direction):
        if index not in APP_INDICES:
            return
        sessions = self.audio.get_sessions()
        if not sessions:
            return
        current = self.channels[index].assigned_session
        other_i = APP_INDICES[0] if index == APP_INDICES[1] else APP_INDICES[1]
        other = self.channels[other_i].assigned_session
        available = [s for s in sessions if s != other]
        if not available:
            return
        try:
            cur = available.index(current) if current in available else -1
            nxt = (cur + direction) % len(available)
            self.channels[index].assigned_session = available[nxt]
            self.channels[index].volume = available[nxt].volume
            self._notify(index)
        except Exception:
            pass

    def get_channel_info(self, index):
        if index < 0 or index >= len(self.channels):
            return None
        ch = self.channels[index]
        t = LAYOUT[index]
        name = "MIC" if t == "INPUT" else ("OBS" if t == "OBS" else ch.display_name)
        icon = "MST" if ch.is_master else ICON_MAP.get((ch.process_name or "").lower(), "UNK")
        if t == "INPUT":
            icon = "MIC"
        elif t == "OBS":
            icon = "OBS"
        return {
            'index': index, 'icon': icon, 'name': (name or "")[:8],
            'volume': int(ch.volume * 100), 'process_name': ch.process_name,
            'process_id': ch.assigned_session.process_id if ch.assigned_session else None,
        }

    def get_all_channel_info(self):
        return [self.get_channel_info(i) for i in range(len(self.channels))]

    def register_change_callback(self, callback):
        self._callbacks.append(callback)

    def _notify(self, index):
        if index < len(self.channels):
            for cb in self._callbacks:
                try:
                    cb(index, self.channels[index])
                except Exception:
                    pass

    def _notify_all(self):
        for i in range(len(self.channels)):
            self._notify(i)


# ── Mixer App ────────────────────────────────────────────────────────────────

class MixerApp:
    def __init__(self, port=None):
        self.audio = AudioController()
        self.serial = SerialProtocol(port=port)
        self.obs = OBSController()
        self.channels = ChannelManager(self.audio, self.obs)
        self.icons = IconExtractor()
        self.eq = EqualizerAPO()

        self._running = False
        self._connected = False
        self._mode = "VOLUME"
        self._sent_icons: Set[str] = set()
        self._tray = None

        self.serial.register_callback(MessageType.VOLUME, self._on_volume)
        self.serial.register_callback(MessageType.SELECT, self._on_select)
        self.serial.register_callback(MessageType.PING, lambda _: self.serial.send_ping())
        self.serial.register_callback(MessageType.MODE, self._on_mode)
        self.channels.register_change_callback(self._on_channel_changed)

    def start(self, use_tray=True):
        self._running = True
        threading.Thread(target=self._monitor, daemon=True).start()
        self.audio.start_monitoring()
        self.obs.connect()
        self.channels.initialize()
        if use_tray and HAS_TRAY:
            self._run_tray()
        else:
            self._run_console()

    def stop(self):
        self._running = False
        self.audio.stop_monitoring()
        self.serial.disconnect()
        if self._tray:
            self._tray.stop()

    def _monitor(self):
        while self._running:
            if not self.serial.is_connected():
                if self._connected:
                    self._connected = False
                    self._sent_icons.clear()
                if self.serial.connect():
                    self._connected = True
                    self._push_all()
            time.sleep(2)

    def _push_all(self):
        if not self.serial.is_connected():
            return
        self._sent_icons.clear()
        infos = self.channels.get_all_channel_info()
        self.serial.send_app_count(len(infos))
        time.sleep(0.1)
        for i, info in enumerate(infos):
            self._push_channel(i, info)
            time.sleep(0.05)

    def _push_channel(self, index, info):
        self.serial.send_app_info(index, info['icon'], info['name'], info['volume'])
        key = f"{index}:{info['process_name'] or 'system'}"
        if key not in self._sent_icons:
            data = self.icons.get_icon(info['process_name'], info['icon'] == "MST")
            if data:
                self.serial.send_icon(index, data)
                self._sent_icons.add(key)

    def _on_volume(self, args):
        if len(args) < 2:
            return
        try:
            ch, vol = int(args[0]), int(args[1])
            if self._mode == "EQ":
                self.eq.set_band_gain(ch, (vol / 100.0 * 30.0) - 15.0)
            else:
                self.channels.set_volume(ch, vol / 100.0)
        except (ValueError, IndexError):
            pass

    def _on_select(self, args):
        if len(args) < 2:
            return
        try:
            ch, d = int(args[0]), int(args[1])
            if self._mode == "VOLUME":
                self.channels.cycle_app(ch, d)
        except (ValueError, IndexError):
            pass

    def _on_mode(self, args):
        if not args:
            return
        self._mode = args[0]
        if self._mode == "EQ":
            self.eq.initialize()
        self._push_all()

    def _on_channel_changed(self, index, channel):
        if self._connected:
            info = self.channels.get_channel_info(index)
            if info:
                self._push_channel(index, info)

    def _run_console(self):
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def _run_tray(self):
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for i, c in enumerate([(100, 200, 255), (100, 255, 150), (255, 200, 100)]):
            x = 10 + i * 18
            draw.rectangle([x, size - 20 - i * 10 - 5, x + 12, size - 5], fill=c)
        menu = pystray.Menu(
            pystray.MenuItem("Custom Mixer", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", lambda: self.stop())
        )
        self._tray = pystray.Icon("mixer", img, "Custom Mixer", menu)
        self._tray.run()


# ── Entry Point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Custom Mixer")
    parser.add_argument("--port", "-p")
    parser.add_argument("--console", "-c", action="store_true")
    parser.add_argument("--test", "-t", action="store_true")
    args = parser.parse_args()

    if args.test:
        a = AudioController()
        print(f"Master: {a.get_master_volume() * 100:.0f}%")
        for s in a.get_sessions():
            print(f"  {s.display_name}: {s.volume * 100:.0f}%")
        return

    MixerApp(port=args.port).start(use_tray=not args.console)

if __name__ == "__main__":
    main()
