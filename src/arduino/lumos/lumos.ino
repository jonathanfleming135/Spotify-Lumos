#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>

#define DOUT 6
#define INTERRUPT_PIN 2
#define NUM_PIXELS 422
#define NUM_PATTERNS 3
#define LED_NUM 0
#define LED_VAL 1


volatile bool changePattern;
int16_t globalCount;

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_RGB     Pixels are wired for RGB bitstream
//   NEO_GRB     Pixels are wired for GRB bitstream
//   NEO_KHZ400  400 KHz bitstream (e.g. FLORA pixels)
//   NEO_KHZ800  800 KHz bitstream (e.g. High Density LED strip)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, DOUT, NEO_GRB + NEO_KHZ800);

void setup() {

    Serial.begin(9600);

    strip.begin();
    strip.show();

    pinMode(INTERRUPT_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), interruptServiceRoutine, CHANGE);

    globalCount = 0;
    changePattern = false;

}

void loop() {
    uint8_t led_colours[NUM_PIXELS];
    read_packet(led_colours);
    write_packet(led_colours);
    //parse_packet(pckt_in, led_colours);
}

void read_packet(uint8_t* led_colours)
{
    uint16_t count = 0;
    uint8_t curr_colour;
    uint8_t curr_led;
    char line[10] = "";
    char* token;

    while(true) {
        if (Serial.available() > 0) {
            if (Serial.read() == '$') {
                //start reading packet
                char curr = ' ';
                while (curr != '*') {
                    if (Serial.available() > 0) {
                        curr = (char) Serial.read();
                        line[count] = curr;
                        if (curr == '\n' && line[0] != '$' && line[0] != '*') {
                            token = strtok(line, ",");
                            curr_led = atoi(token);
                            token = strtok(NULL, ",");
                            curr_colour = atoi(token);
                            led_colours[curr_led] = curr_colour;
                            count = 0;
                        }
                        else
                            count++;
                    }
                }
                break;
            }
        }
    }

    //int i;
    //for(i = 1; i < 7; i++) {
    //    Serial.println(led_colours[i]);
    //}
}

void write_packet(uint8_t* led_colours)
{
    int16_t i;
    for (i = 0; i < 7; i++) {
        strip.setPixelColor(i, colourWheel((byte) led_colours[i]));
        Serial.print(i);
        Serial.print(",");
        Serial.println((byte) led_colours[i]);
    }
    strip.show();
}

uint32_t colourWheel(byte value) {
    if(value < 85) {
        return (strip.Color(round((value * 3)/4), round((255 - (value * 3))/4), 0) );
    } else if(value < 170) {
        value -= 85;
        return (strip.Color(round((255 - (value * 3))/4), 0, round((value * 3)/4)) );
    } else {
        value -= 170;
        return (strip.Color(0, round((value * 3)/4), round((255 - (value * 3))/4)) );
    }
}

void interruptServiceRoutine() {
  changePattern = true;
}
