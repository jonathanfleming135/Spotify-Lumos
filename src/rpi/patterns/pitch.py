import arduino_control as arduino
import constants as const
import random as rand
import time
import utils as util
import spotify_api_requests as spot_api

COLOURS_PER_PITCH = const.NUM_COLOURS / const.NUM_PITCHES

def pattern(progress, duration):
	'''
	Performs the pitch pattern for the duration specified

	@param progress - the progress made in the currently playing song
	@param duration - the duration this pattern should run for
	'''
	segments = spot_api.get_song_analysis()["segments"]

	while (progress < duration and len(segments) > 0):
		while (segments[0]["start"] < progress):
			segments.pop(0)

		pitches = segments[0]["pitches"]
		colour = get_colour_from_pitches(pitches)
		LEDs = [(0, colour, const.ALL_LEDS)]
		arduino.write_packet(LEDs)

		progress += segments[0]["duration"]
		util.sleep(segments[0]["duration"] * 1000.0)

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