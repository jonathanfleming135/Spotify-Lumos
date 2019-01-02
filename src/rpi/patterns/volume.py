import arduino_control as arduino
import constants as const
import utils as util
import spotify_api_requests as spot_api

def pattern(duration, analysis):
	'''
	Performs the volume pattern for the duration specified

	@param duration - duration this pattern should run for (seconds)
	@param analysis - song analysis returned from the spotify api call
	'''
	prep_time_start = util.clock()
	util.clear_leds()

	segments = analysis["segments"]
	max_loudness = get_max_loudness(segments)
	min_loudness = get_min_loudness(segments)
	max_loudness_diff = max_loudness - min_loudness

	progress = spot_api.get_song_progress()
	prep_time_end = util.clock()
	prep_time = prep_time_end - prep_time_start
	duration += progress - (prep_time / 1000.0)

	while (len(segments) > 0 and segments[0]["start"] < progress):
		segments.pop(0)

	if (len(segments) > 1):
		init_time_diff = progress - segments[0]["start"]
		util.sleep(init_time_diff * 1000.0)
		segments.pop(0)

	prev_colour = 0
	prev_loudness_percent = 0
	while (progress < duration and len(segments) > 1):
		curr_segment_time_start = util.clock()

		curr_segment = segments[0]
		next_segment = segments[1]

		loudness = (curr_segment["loudness_start"] + next_segment["loudness_start"]) / 2.0
		loudness_diff = loudness - min_loudness
		loudness_percent = loudness_diff / max_loudness_diff

		pitches = curr_segment["pitches"]
		colour = get_colour_from_pitches(pitches)

		if (curr_segment["confidence"] <= 0.1):
			colour = prev_colour
			loudness_percent = prev_loudness_percent

		write_leds(colour, loudness_percent)

		curr_segment_time_end = util.clock()
		segment_time_diff = curr_segment_time_end - curr_segment_time_start
		sleep_time = (curr_segment["duration"] * 1000.0) - segment_time_diff

		progress += segments[0]["duration"]

		util.sleep(sleep_time)

		while (len(segments) > 0 and segments[0]["start"] < progress):
			segments.pop(0)

		prev_colour = colour
		prev_loudness_percent = loudness_percent

def write_leds(colour, loudness_percent):
	'''
	Helper function to write the led values to the arduino

	@param colour - the colour value to write
	@param loudness_percent - loudness as a percent of the max loudness
	'''
	max_led_slice = (const.CORNER_ONE - const.CORNER_ZERO) / 2.0
	led_slice = int(round(loudness_percent * max_led_slice))

	LEDs = []
	if (loudness_percent >= 1.0):
		LEDs.append(const.CORNER_ZERO, colour, const.ALL_LEDS)
	elif (loudness_percent <= 0.0):
		LEDs.append((const.CORNER_ZERO, const.BLACK, const.CORNER_ONE))
		LEDs.append((const.CORNER_ONE, colour, const.CORNER_TWO))
		LEDs.append((const.CORNER_TWO, const.BLACK, const.CORNER_THREE))
		LEDs.append((const.CORNER_THREE, colour, const.CORNER_FOUR))
	else:
		LEDs.append((const.CORNER_ZERO, colour, led_slice))
		LEDs.append((led_slice, const.BLACK, const.CORNER_ONE - led_slice))
		LEDs.append((const.CORNER_ONE - led_slice, colour, const.CORNER_TWO + led_slice))
		LEDs.append((const.CORNER_TWO + led_slice, const.BLACK, const.CORNER_THREE - led_slice))
		LEDs.append((const.CORNER_THREE - led_slice, colour, const.CORNER_FOUR))
	arduino.write_packet(LEDs)

def get_max_loudness(segments):
	'''
	Helper function to retrieve the max loudness of the song

	@param segments - the list of segments as returned from the spotify api request
	@return max loudness_max property amongst all segments
	'''
	# loudness should never be below -100 db
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
	@return min loudness_min property amongst all segments
	'''
	# loudness should never be above 100 db
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
	@return colour value (0-255)
	'''
	COLOURS_PER_PITCH = const.NUM_COLOURS / const.NUM_PITCHES

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
