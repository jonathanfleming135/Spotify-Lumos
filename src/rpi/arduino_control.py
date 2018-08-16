#!/usr/bin/python
import serial
import subprocess
import time

NUM_LEDS = 442

def main():
    #serialPort = serial.Serial("/dev/ttyACM0", baudrate=115200)
    #subprocess.Popen(["/home/pi/spotify-lumos/src/scripts/arduino_startup.sh"])
    serialPort = serial.Serial()
    serialPort.baudrate = 115200
    serialPort.port = '/dev/ttyACM0'
    serialPort.open()
    serialPort.write("\r\n".encode())
    print(serialPort.is_open)
    LEDs = []

    for LED in range (0, NUM_LEDS):
        LEDs.append((LED, 40))

    #packet = encode_packet(LEDs)
    #serialPort.write(packet.encode())
    write_packet(LEDs, serialPort)
    #serialPort.close()

'''
Writes a list of led values to the Arduino

@param[in]  LED_values
'''
def write_packet(LED_values, port):
    packet = encode_packet(LED_values)
    print(port.write(packet.encode()))

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


if __name__ == '__main__':
    main()