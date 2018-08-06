#!/usr/bin/python
import json
import serial

NUM_LEDS = 5

def main():
    serialPort = serial.Serial("/dev/ttyACM0", baudrate=9600)

    LED1 = (1, 50)
    LED2 = (2, 100)
    LED3 = (3, 150)
    LED4 = (4, 200)
    LED5 = (5, 250)
    LED6 = (6, 300)

    LEDs = [LED1, LED2, LED3, LED4, LED5, LED6]

    packet = encode_packet(LEDs)
    serialPort.write(packet.encode())
    print(packet)

def encode_packet(LED_values):
    packet = ""
    for LED in LED_values:
        packet += str(LED[0])
        packet += ','
        packet += str(LED[1])
        packet += '\n'

    '''
    json_LEDs = []
    for LED in LED_values:
        json_LEDs.append(
                        {
                            "LED_num": LED[0],
                            "value": LED[1]
                        })

    json_obj = {
                    "LEDs": json_LEDs
    }

    packet = json.dumps(json_obj, sort_keys=True, indent=4, separators=(',', ': '))
    '''
    packet = "$\n" + packet + "*"

    return packet


if __name__ == '__main__':
    main()