#!/usr/bin/python
import arduino_control as arduino
import constants as const
import spotify_api_requests as spot_api
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


	next_check_time = 0.0
	next_print_time = 0.0
	while(True):
		volume.pattern(5)
		shimmer.pattern(10)
		if(time.clock() > next_check_time):
			spot_api.check_currently_playing_song()
			next_check_time = time.clock() + 3.0

		if(time.clock() > next_print_time):
			print(spot_api.get_song_features())
			next_print_time = time.clock() + 10.0
		pass

if __name__ == '__main__':
    main()
