import arduino_control as arduino
import constants as const
import random as rand
import time
import utils as util
import spotify_api_requests as spot_api

def pattern(progress, duration):
	'''
	Performs the volume pattern for the duration specified

	@param progress - the progress made in the currently playing song
	@param duration - the duration this pattern should run for
	'''
	segments = spot_api.get_song_analysis()["segments"]
	max_loudness = get_max_loudness(segments)
	min_loudness = get_min_loudness(segments)
	loudness_diff = max_loudness - min_loudness

	while (progress < duration and len(segments) > 0):
		while (segments[0]["start"] < progress):
			segments.pop(0)

		curr_segment = segments[0]

		curr_loudness = curr_segment["loudness_max"]
		curr_loudness_diff = curr_loudness - min_loudness
		loudness_percent = curr_loudness_diff / loudness_diff

		num_leds = round(loudness_percent * (const.CORNER_ONE - const.CORNER_ZERO))
		LEDs = []
		opposite_led = const.CORNER_THREE - num_leds
		LEDs.append(const.CORNER_ZERO, const.RED, num_leds)
		LEDs.append(opposite_led, const.RED, num_leds)
		arduino.write_packet(LEDs)

		progress += segments[0]["duration"]
		util.sleep(segments[0]["duration"] * 1000.0)

def get_max_loudness(segments):
	'''
	Helper function to retrieve the max loudness of the song

	@param segments - the list of segments as returned from the spotify api request
	'''
	max_loudness = -100.0
	for i in range(0, len(segments)):
		curr_loudness = segments[i]["loudness_max"]
		if (curr_loudness > max_loudness):
			max_loudness = curr_loudness
	return max_loudness

def get_min_loudness(segments):
	'''
	Helper function to retrieve the min loudness of the song

	@param segments - the list of segments as returned from the spotify api request
	'''
	min_loudness = 100.0
	for i in range(0, len(segments)):
		curr_loudness = segments[i]["loudness_max"]
		if (curr_loudness < min_loudness):
			min_loudness = curr_loudness
	return min_loudness
