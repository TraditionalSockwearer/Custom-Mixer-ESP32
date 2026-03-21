# boot.py - Enable USB CDC data port for serial communication
import usb_cdc
usb_cdc.enable(console=True, data=True)
