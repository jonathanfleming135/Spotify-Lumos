import time
import arduino_control as arduino
import constants as const

# Calculates time to wait for a given number of lines, calculation based
# on measured values. Each line represents a single line of text in the packet
# to be sent over serial
#
# @param[in]  num_leds
# @return     time to wait (ms) before writing to led's again
def time_to_next_write(num_lines):
    return round(const.WAIT_PER_LED * num_lines + 20)

# Calculates the max number of lines that can be written given a wait time.
# Inverse of time_to_next_write, calculation based on measured values
#
# @param[in]  wait_time (ms)
# #return     max amount of led's that can be written to
def max_lines_per_write(wait_time):
    if (wait_time <= 20):
        return 0
    else:
        return round((1/const.WAIT_PER_LED) * (wait_time - 20))

# Sleeps for a given amount of ms without stopping the clock
#
# @param[in]  time_ms
def sleep(time_ms):
	start_time = clock()
	while (clock() < start_time + time_ms ):
		pass

# Sets all led's to off
def clear_leds():
    LEDs = []
    LEDs.append((0, 0, const.ALL_LEDS))
    arduino.write_packet(LEDs)

# returns clock time in ms
def clock():
    return time.clock() * 1000.0