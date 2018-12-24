#!/usr/bin/python
import arduino_control as arduino
import constants as const
import spotify_api_requests as spot_api
import time
import pprint
from patterns import *

def main():
	# initalize serial port with arduino
	arduino.init_port()

	next_check_time = 0.0
	while(True):
		if(time.clock() > next_check_time):
			spot_api.check_currently_playing_song()
			next_check_time = time.clock() + 3.0

		song_progress = spot_api.get_song_progress()
		song_duration = spot_api.get_song_features()["duration_ms"] / 1000.0
		pitch.pattern(song_progress, song_duration - song_progress)

		pass

if __name__ == '__main__':
    main()
