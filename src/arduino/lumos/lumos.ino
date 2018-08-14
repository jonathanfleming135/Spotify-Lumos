#include <Adafruit_NeoPixel.h>

#define DOUT 6
#define NUM_PIXELS 422
#define LED_NUM 0
#define LED_VAL 1
#define MAX_BAUD 115200
#define MAX_LINE_LEN 10
#define START_CHAR '$'
#define TERM_CHAR '*'

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_RGB     Pixels are wired for RGB bitstream
//   NEO_GRB     Pixels are wired for GRB bitstream
//   NEO_KHZ400  400 KHz bitstream (e.g. FLORA pixels)
//   NEO_KHZ800  800 KHz bitstream (e.g. High Density LED strip)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, DOUT, NEO_GRB + NEO_KHZ800);

void setup() {
    Serial.begin(MAX_BAUD);
    strip.begin();
}

void loop() {
    uint8_t led_colours[NUM_PIXELS];
    read_packet(led_colours);
    write_packet(led_colours);
}

/**
  * Polls for a packet to be available, then parses the packet as it comes in,
  * line by line.
  *
  * @param[out] led_colours
  */
void read_packet(uint8_t* led_colours)
{
    uint8_t count = 0;
    char line[MAX_LINE_LEN] = "";

    wait_for_packet_start();
    char curr = ' ';
    while (curr != TERM_CHAR) {
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

/**
  * Polls for a packet to be available, helper func for read_packet
  */
void wait_for_packet_start() {
    while (true) {
        if (Serial.available() > 0) {
            if (Serial.read() == START_CHAR) {
                return;
            }
        }
    }
}

/**
  * Parses a single line from an incoming packet, helper func for read_packet
  *
  * @param[in]  line
  * @param[out] led_colours
  */
void parse_line(char* line, uint8_t* led_colours)
{
    uint8_t curr_colour;
    uint16_t curr_led;
    char* token;

    if (line[0] == START_CHAR || line[0] == TERM_CHAR) {
        return;
    } else {
        token = strtok(line, ",");
        curr_led = atoi(token);
        token = strtok(NULL, ",");
        curr_colour = atoi(token);
        led_colours[curr_led] = curr_colour;
    }
}

/**
  * Iterates through all led_colours and writes the entire array to the led
  * strip
  *
  * @param[in]  led_colours
  */
void write_packet(uint8_t* led_colours)
{
    uint16_t i;
    for (i = 0; i < NUM_PIXELS; i++) {
        strip.setPixelColor(i, colourWheel((byte) led_colours[i]));
    }
    strip.show();
}

/**
  * Used to convert a byte value to a colour value for the led strip
  *
  * @param[in]  value
  */
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
