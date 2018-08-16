#!/usr/bin/python
import arduino_control as arduino
import constants as const

def main():
	port = arduino.init_port()

	LEDs = []

	for LED in range (0, const.CORNER_ONE):
		LEDs.append((LED, 50))

	for LED in range (const.CORNER_ONE, const.CORNER_TWO):
		LEDs.append((LED, 100))

	for LED in range (const.CORNER_TWO, const.CORNER_THREE):
		LEDs.append((LED, 250))

	for LED in range (const.CORNER_THREE, const.CORNER_FOUR):
		LEDs.append((LED, 200))

	arduino.write_packet(LEDs, port)

	while(True):
		#idle for now
		pass

if __name__ == '__main__':
    main()