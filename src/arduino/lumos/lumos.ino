#include <Adafruit_NeoPixel.h>

#define DOUT 6
#define NUM_PIXELS 422
#define LED_NUM 0
#define LED_VAL 1

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
}

void loop() {
    uint8_t led_colours[NUM_PIXELS];
    read_packet(led_colours);
    write_packet(led_colours);
    Serial.println(millis());
}

void read_packet(uint8_t* led_colours)
{
    uint8_t count = 0;
    char line[10] = "";

    wait_for_packet_start();
    //start reading packet
    Serial.println(millis());
    char curr = ' ';
    while (curr != '*') {
        if (Serial.available() > 0) {
            curr = (char) Serial.read();
            line[count] = curr;
            if (curr == '\n') {
                parse_line(line, led_colours);
                count = 0;
            }
            else
                count++;
        }
    }
}

void wait_for_packet_start() {
    while (true) {
        if (Serial.available() > 0) {
            if (Serial.read() == '$') {
                return;
            }
        }
    }
}

void parse_line(char* line, uint8_t* led_colours)
{
    uint8_t curr_colour;
    uint16_t curr_led;
    char* token;

    if (line[0] == '$' || line[0] == '*') {
        return;
    } else {
        token = strtok(line, ",");
        curr_led = atoi(token);
        token = strtok(NULL, ",");
        curr_colour = atoi(token);
        led_colours[curr_led] = curr_colour;
    }
}

void write_packet(uint8_t* led_colours)
{
    uint16_t i;
    for (i = 0; i < NUM_PIXELS; i++) {
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
