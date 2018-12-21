import arduino_control as arduino
import constants as const
import random as rand
import utils as util

def pattern(run_time):
	LEDs = []
	LEDs.append((0, 50, const.ALL_LEDS))
	arduino.write_packet(LEDs)