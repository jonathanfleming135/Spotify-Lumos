#!/usr/bin/python
import arduino_control as arduino
import constants as const
import time
from patterns import *

def main():
	# initalize serial port with arduino
	arduino.init_port()

	LEDs = []
	LEDs.append((0, 200, const.ALL_LEDS))

	arduino.write_packet(LEDs)

	LEDs.append((0, 250, const.ALL_LEDS))

	arduino.write_packet(LEDs)



	while(True):
		shimmer.pattern(10)
		pass

if __name__ == '__main__':
    main()
