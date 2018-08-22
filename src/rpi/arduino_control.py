#!/usr/bin/python
import serial
import constants as const

# Initializes Serial port for communication with Arduino
def init_port():
    return serial.Serial('/dev/ttyACM0', 115200)

# Writes a list of led values to the Arduino
#
# @param[in]  LED_values
def write_packet(LED_values, port):
    packet = encode_packet(LED_values)
    port.write(packet.encode())

# Encodes a packet to send to the Arduino
def encode_packet(LED_values):
    packet = ""
    for LED in LED_values:
        packet += str(LED[0])
        packet += ','
        packet += str(LED[1])
        packet += '\n'
    packet = "$\n" + packet + "*"
    return packet

# Calculates time to wait for a given number of led's, calculation based
# on measured values
#
# @param[in]  num_leds
# @return     time to wait (ms) before writing to led's again
def time_to_next_write(num_leds):
    return round(const.WAIT_PER_LED * num_leds + 20)

# Calculates the max number of leds that can be written given a wait time.
# Inverse of time_to_next_write, calculation based on measured values
#
# @param[in]  wait_time (ms)
# #return     max amount of led's that can be written to
def max_leds_per_write(wait_time):
    if (wait_time <= 20):
        return 0
    else:
        return round((1/const.WAIT_PER_LED) * (wait_time - 20))
