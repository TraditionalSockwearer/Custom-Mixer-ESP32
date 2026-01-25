import time
import board
import analogio
import rotaryio
import keypad
import adafruit_ssd1306
import adafruit_tca9548a
import adafruit_ble
import displayio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
import adafruit_ble_midi
from adafruit_ble_midi.control_change import ControlChange
from adafruit_ble_midi.note_on import NoteOn
from adafruit_ble_midi.note_off import NoteOff

FADER_PINS = (
    board.IO32,
    board.IO33,
    board.IO34,
    board.IO35,
    board.IO36
)

ENCODER_ROTARY_PINS = (
    (board.IO25, board.IO26),
    (board.IO14, board.IO12)
)

ENCODER_SWITCH_PINS = (
    board.IO27,
    board.IO13
)

LABELS = ["MASTER", "CHROME", "DISCORD", "SPOTIFY", "GAME"]

displayio.release_displays()

i2c = board.I2C()

mux = adafruit_tca9548a.TCA9548A(i2c)

screens = []
for i in range(5):
    try:
        display = adafruit_ssd1306.SSD1306_I2C(128, 32, mux[i], addr=0x3C)
        display.fill(0)
        display.text(f"Init Ch {i+1}...", 0, 0, 1)
        display.show()
        screens.append(display)
    except ValueError:
        print(f"Screen {i+1} missing or I2C error.")
        screens.append(None)

faders = [analogio.AnalogIn(pin) for pin in FADER_PINS]

encoders = [rotaryio.IncrementalEncoder(pin_a, pin_b) for pin_a, pin_b in ENCODER_ROTARY_PINS]

keys = keypad.Keys(ENCODER_SWITCH_PINS, value_when_pressed=False, pull=True)

ble = adafruit_ble.BLERadio()
midi_service = adafruit_ble_midi.MIDIBService()
advertisement = ProvideServicesAdvertisement(midi_service)
advertisement.complete_name = "ESP32 Mixer Interface"

def get_smooth_val(analog_in, samples=20):
    total = 0
    for _ in range(samples):
        total += analog_in.value
    return total // samples

def update_screen(index, value_0_to_1):
    display = screens[index]
    if display is None:
        return
    
    display.fill(0)
    display.text(LABELS[index], 0, 0, 1)
    display.rect(0, 12, 128, 16, 1)
    width = int(value_0_to_1 * 126)
    display.fill_rect(2, 14, width, 12, 1)
    display.show()

print("Waiting for Bluetooth connection...")

last_midi_vals = [-1] * 5
last_enc_pos = [0] * len(encoders)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    
    print("Bluetooth Connected")
    
    while ble.connected:
        for i, fader in enumerate(faders):
            raw_val = get_smooth_val(fader)
            midi_val = int((raw_val / 65535) * 127)
            
            if abs(midi_val - last_midi_vals[i]) > 1:
                try:
                    midi_service.write(ControlChange(i, midi_val))
                    update_screen(i, raw_val / 65535)
                    last_midi_vals[i] = midi_val
                except OSError:
                    break

        for i, enc in enumerate(encoders):
            current_pos = enc.position
            change = current_pos - last_enc_pos[i]
            
            if change != 0:
                cc_number = 20 + i
                val_to_send = 127 if change > 0 else 1
                
                try:
                    midi_service.write(ControlChange(cc_number, val_to_send))
                except OSError:
                    break
                
                last_enc_pos[i] = current_pos

        event = keys.events.get()
        if event:
            key_number = event.key_number
            cc_number = 30 + key_number
            
            try:
                if event.pressed:
                    midi_service.write(NoteOn(cc_number, 127))
                elif event.released:
                    midi_service.write(NoteOff(cc_number, 0))
            except OSError:
                break
        
        time.sleep(0.01)
