#!/usr/bin/python
import serial
import time
import constants as const
import utils as util

def init_port():
    '''
    Initializes Serial port for communication with Arduino
    '''
    global port
    port = serial.Serial('/dev/ttyACM0', 115200)

def write_packet(LED_values):
    '''
    Writes a list of led values to the Arduino, waits till the next available led
    write time without stopping the clock

    @param[in]  LED_values
    '''
    packet = encode_packet(LED_values)
    port.write(packet.encode())
    sleep_time = util.time_to_next_write(len(LED_values))
    util.sleep(sleep_time)

def encode_packet(LED_values):
    '''
    Encodes a packet to send to the Arduino
    '''
    packet = ""
    for LED in LED_values:
        packet += str(LED[0])
        packet += ','
        packet += str(LED[1])
        if (len(LED) == 3):
            packet += ','
            packet += str(LED[2])
        packet += '\n'
    packet = "$\n" + packet + "*"
    return packet
