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
    char pckt_in[1000] = "";
    read_packet(pckt_in);
    char pckt[1000] = "";
    parse_packet(pckt_in);
}

void read_packet(char* pckt_in)
{
    int32_t count = 0;

    while(true) {
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
                break;
            }
        }
    }

    pckt_in[count] = '\0';
    pckt_in[count-1] = '\0';
}

void parse_packet(char* pckt_in)
{
    char *line;
    int curr = LED_NUM;

    line = strtok(pckt_in, "\n,");
    while (line != NULL) {
        switch(curr) {
            case LED_NUM:
                Serial.print("num: ");
                Serial.println(line);
                curr = LED_VAL;
                break;
            case LED_VAL:
                Serial.print("val: ");
                Serial.println(line);
                curr = LED_NUM;
                break;
        }

        line = strtok(NULL, "\n,");
    }

    //const size_t bufferSize = JSON_ARRAY_SIZE(6) + JSON_OBJECT_SIZE(1) + 6*JSON_OBJECT_SIZE(2) + 140;
    //DynamicJsonBuffer jsonBuffer(bufferSize);

    /*

    StaticJsonBuffer<2000> jsonBuffer;

    Serial.print(pckt_in);

    delay(1000);

    JsonObject& root = jsonBuffer.parseObject(pckt_in);

    JsonArray& LEDs = root["LEDs"];

    if (!root.success()) {
        Serial.println("parseObject() failed");
        return;
    }

    int LEDs0_LED_num = LEDs[0]["LED_num"]; // 1
    int LEDs0_value = LEDs[0]["value"]; // 50

    int LEDs1_LED_num = LEDs[1]["LED_num"]; // 2
    int LEDs1_value = LEDs[1]["value"]; // 100

    int LEDs2_LED_num = LEDs[2]["LED_num"]; // 3
    int LEDs2_value = LEDs[2]["value"]; // 150

    int LEDs3_LED_num = LEDs[3]["LED_num"]; // 4
    int LEDs3_value = LEDs[3]["value"]; // 200

    Serial.println(LEDs2_value);

    */

    /*
    Serial.print(pckt_in);
    StaticJsonBuffer<2000> jsonBuffer;
    JsonObject &root = jsonBuffer.parseObject(pckt_in);

    if (!root.success()) {
        Serial.println("parseObject() failed");
        return;
    }

    int led1 = root["LEDs"][0]["LED_num"];
    int val1 = root["LEDs"][0]["value"];
    //Serial.print("led1: ");
    //Serial.println(led1);
    //Serial.print("val1: ");
    //Serial.println(val1);
    */
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
