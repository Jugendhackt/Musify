import time
import rtmidi
import random

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    midiout.open_port(1) # loopMIDI Port 1 (zweiter Port im Array)
else:
    midiout.open_virtual_port("My virtual output")

with midiout:
    # channel 1, middle C, velocity 112
    for _ in range(0, 100):
        control = [0xB0, 23, random.randrange(0, 127, 1)]
        midiout.send_message(control)
        control = [0xB0, 37, 127]
        midiout.send_message(control)
        control = [0xB0, 24, random.randrange(0, 127, 1)]
        midiout.send_message(control)
        time.sleep(0.5)

    time.sleep(0.1)
del midiout