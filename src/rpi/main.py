#!/usr/bin/python
import arduino_control as arduino
import constants as const

def main():
	# initalize serial port with arduino
	port = arduino.init_port()

	LEDs = []
	for LED in range (0, const.ALL_LEDS):
		LEDs.append((LED, 200))

	arduino.write_packet(LEDs, port)

	for LED in range (0, const.ALL_LEDS):
		LEDs.append((LED, 250))

	arduino.write_packet(LEDs, port)

	while(True):
		pass

if __name__ == '__main__':
    main()
