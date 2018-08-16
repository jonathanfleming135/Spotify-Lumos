#!/usr/bin/python
import serial

'''
Initializes Serial port for communication with Arduino
'''
def init_port():
    return serial.Serial('/dev/ttyACM0', 115200)

'''
Writes a list of led values to the Arduino
@param[in]  LED_values
'''
def write_packet(LED_values, port):
    packet = encode_packet(LED_values)
    port.write(packet.encode())

'''
Encodes a packet to send to the Arduino
'''
def encode_packet(LED_values):
    packet = ""
    for LED in LED_values:
        packet += str(LED[0])
        packet += ','
        packet += str(LED[1])
        packet += '\n'

    packet = "$\n" + packet + "*"

    return packet
