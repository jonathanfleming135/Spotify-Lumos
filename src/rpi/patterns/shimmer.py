import arduino_control as arduino
import constants as const
import random as rand
import utils as util

def pattern(run_time):
	run_time = run_time * 1000.0
	start_time = util.clock()

	num_leds = round(const.ALL_LEDS / 10.0)
	time_between_writes = 125

	num_leds = min(util.max_lines_per_write(time_between_writes), num_leds)

	while (start_time + run_time > util.clock() ):
		write_time = util.clock()
		util.clear_leds()

		LEDs = []
		for led in range (0, num_leds):
			curr_led = rand.randint(0, const.ALL_LEDS)
			if ((curr_led, const.WHITE) not in LEDs):
				LEDs.append((curr_led, const.WHITE))

		arduino.write_packet(LEDs)
		time_already_waited = util.clock() - write_time
		util.sleep(time_between_writes - time_already_waited)
