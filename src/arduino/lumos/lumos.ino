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

    char buffer[10000];

    while(1) {
        if (Serial.available() > 0) {
            char incomingByte = Serial.read();
            if (incomingByte == '$') {
                int count = 0;
                while (incomingByte != '*') {
                    if (Serial.available() > 0) {
                        buffer[count] = Serial.read();
                        incomingByte = buffer[count];
                        Serial.print(buffer[count]);
                        count++;
                    }
                }
                Serial.println("erg");

                buffer[count-1] = '\r';
                buffer[count] = '\r';

                int pcount;
                for(pcount = 0; pcount < count; pcount++) {
                    Serial.print(buffer[pcount]);
                    delay(2);
                }

                //delay(10);
                Serial.println("line 63");
                //delay(10);

                StaticJsonBuffer<1000> jsonBuffer;
                JsonObject &root = jsonBuffer.parseObject(buffer);

                //delay(10);
                Serial.println("line 66");
                //delay(10);

                if (!root.success()) {
                    Serial.println("parseObject() failed");
                    continue;
                }

                //delay(10);
                Serial.println("line 71");
                //delay(10);

                int led1 = root["LEDs"][0]["LED_num"];
                int val1 = root["LEDs"][0]["value"];
                Serial.print("led1: ");
                Serial.println(led1);
                delay(10);
                Serial.print("val1: ");
                Serial.println(val1);

                //int pcount;
                //for(pcount = 0; pcount < count-1; pcount++) {
                //    Serial.print(buffer[pcount]);
                //    delay(2);
                //}
            }
        }
    }
    /*
    StaticJsonBuffer<200> jsonBuffer;

JsonObject& root = jsonBuffer.parseObject(json);

const char* sensor = root["sensor"];
long time          = root["time"];
double latitude    = root["data"][0];
double longitude   = root["data"][1];
    */

        uint16_t patternSel = globalCount % int(NUM_PATTERNS);

        switch(patternSel) {
            case 0:
                rainbow();
                break;
            case 1:
                fillUp();
                break;
            case 2:
                colourSpin();
                break;
            default:
                rainbow();
                break;
        }

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
