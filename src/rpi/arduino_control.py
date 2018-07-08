#!/usr/bin/python
import json
import pprint

NUM_LEDS = 5

def main():
    LED1 = (1, 50)
    LED2 = (2, 100)
    LED3 = (3, 150)
    LED4 = (4, 200)
    LED5 = (5, 250)

    LEDs = [LED1, LED2, LED3, LED4, LED5]

    Set_LEDs(LEDs)

def Set_LEDs(LED_values):
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

    print(json.dumps(json_obj, sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()