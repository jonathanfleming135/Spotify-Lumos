import arduino_control as arduino
import constants as const
import random as rand
import time
import utils as util
import spotify_api_requests as spot_api
# import pitch

COLOURS_PER_PITCH = const.NUM_COLOURS / const.NUM_PITCHES

def pattern(progress, duration):
	'''
	Performs the volume pattern for the duration specified

	@param progress - the progress made in the currently playing song
	@param duration - the duration this pattern should run for
	'''
	util.clear_leds()

	segments = spot_api.get_song_analysis()["segments"]
	max_loudness = get_max_loudness(segments)
	min_loudness = get_min_loudness(segments)
	loudness_diff = max_loudness - min_loudness

	while (progress < duration and len(segments) > 0):
		while (segments[0]["start"] < progress):
			segments.pop(0)

		curr_segment = segments[0]

		curr_loudness = (curr_segment["loudness_start"] + segments[1]["loudness_start"]) / 2.0
		curr_loudness_diff = curr_loudness - min_loudness
		loudness_percent = curr_loudness_diff / loudness_diff

		# print(loudness_percent)
		num_leds = int(round(loudness_percent * ((const.CORNER_ONE - const.CORNER_ZERO)/2.0)))
		LEDs = []
		opposite_led = const.CORNER_THREE - num_leds

		pitches = curr_segment["pitches"]
		colour = get_colour_from_pitches(pitches)

		LEDs.append((const.CORNER_ZERO, colour, num_leds))
		LEDs.append((num_leds, const.BLACK, const.CORNER_ONE - num_leds))
		LEDs.append((const.CORNER_ONE - num_leds, colour, const.CORNER_TWO + num_leds))
		LEDs.append((const.CORNER_TWO + num_leds, const.BLACK, const.CORNER_THREE - num_leds))
		LEDs.append((const.CORNER_THREE - num_leds, colour, const.CORNER_FOUR))

		# LEDs.append((num_leds, const.BLACK, const.CORNER_TWO + (const.CORNER_ONE - num_leds) ))
		# LEDs.append((const.CORNER_TWO + (const.CORNER_ONE - num_leds), colour, const.CORNER_FOUR))
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

def get_pitch_index(pitches):
	'''
	Helper function to retrieve the current pitch

	@param pitches - the list of pitches as return from the spotify api request
	@return pitch index (corresponds to pitch of the note being played)
	'''
	for i in range(0, len(pitches)):
		if (pitches[i] == 1.0):
			return i

def get_colour_from_pitches(pitches):
	'''
	Get's the colour corresponding to the pitch of the sound

	@param pitches - the list of pitches as return from the spotify api request
	@return colour
	'''

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

	colour = round(colour)

	# avoid using special colour values
	if (colour == 0 or colour == 255):
		colour += 1

	return colour
