import arduino_control as arduino
import constants as const
import random as rand
import time
import utils as util
import spotify_api_requests as spot_api

COLOURS_PER_PITCH = const.NUM_COLOURS / const.NUM_PITCHES

def pattern(progress, duration):
	segments = spot_api.get_song_analysis()["segments"]

	while (progress < duration and len(segments) > 0):
		while (segments[0]["start"] < progress):
			segments.pop(0)

		pitches = segments[0]["pitches"]
		pitch_index = get_pitch_index(pitches)

		pitch_index_above = (pitch_index + 1) % (const.NUM_PITCHES - 1)
		pitch_index_below = (pitch_index - 1) % (const.NUM_PITCHES - 1)

		pitch_above = pitches[pitch_index_above]
		pitch_below = pitches[pitch_index_below]

		colour = pitch_index * COLOURS_PER_PITCH

		if (pitch_above > pitch_below):
			colour_diff = (COLOURS_PER_PITCH / 2.0) * pitches[pitch_index_above]
			colour += colour_diff
		elif (pitch_below > pitch_above):
			colour_diff = (COLOURS_PER_PITCH / 2.0) * pitches[pitch_index_below]
			colour -= colour_diff
		else:
			colour = COLOURS_PER_PITCH * pitch_index

		colour_int = round(colour)
		if (colour_int == 0 or colour_int == 255):
			colour_int += 1

		print(colour_int)
		LEDs = [(0, colour_int, const.ALL_LEDS)]
		arduino.write_packet(LEDs)

		progress += segments[0]["duration"]
		util.sleep(segments[0]["duration"] * 1000.0)

def get_pitch_index(pitches):
	i = 0
	for i in range(0, len(pitches)):
		if (pitches[i] == 1.0):
			return i

