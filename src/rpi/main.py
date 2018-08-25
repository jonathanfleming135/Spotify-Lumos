#!/usr/bin/python
import arduino_control as arduino
import constants as const
from patterns import *

def main():
	# initalize serial port with arduino
	port = arduino.init_port()

	LEDs = []
	LEDs.append((0, 200, const.ALL_LEDS))

	arduino.write_packet(LEDs, port)

	LEDs.append((0, 250, const.ALL_LEDS))

	arduino.write_packet(LEDs, port)

	shimmer.pattern()

	while(True):
		pass

if __name__ == '__main__':
    main()
