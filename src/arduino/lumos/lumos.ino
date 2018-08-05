#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>

#define DOUT 6
#define INTERRUPT_PIN 2
#define NUM_PIXELS 422
#define NUM_PATTERNS 3

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
    char pckt_in[1000] = "";
    read_packet(pckt_in);
    Serial.print(pckt_in);
}

void read_packet(char* pckt_in)
{
    int32_t count = 0;

    if (Serial.available() > 0) {
        if (Serial.read() == '$') {
            //start reading packet
            char curr = ' ';
            while (curr != '*') {
                if (Serial.available() > 0) {
                    curr = (char) Serial.read();
                    pckt_in[count] = curr;
                    count++;
                }
            }
        }
    }

    pckt_in[count] = '\0';
    pckt_in[count-1] = '\0';
}


    /*
    StaticJsonBuffer<200> jsonBuffer;

JsonObject& root = jsonBuffer.parseObject(json);

const char* sensor = root["sensor"];
long time          = root["time"];
double latitude    = root["data"][0];
double longitude   = root["data"][1];
    */

//        uint16_t patternSel = globalCount % int(NUM_PATTERNS);
//
//        switch(patternSel) {
//            case 0:
//                rainbow();
//                break;
//            case 1:
//                fillUp();
//                break;
//            case 2:
//                colourSpin();
//                break;
//            default:
//                rainbow();
//                break;
//        }
//
//}

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
