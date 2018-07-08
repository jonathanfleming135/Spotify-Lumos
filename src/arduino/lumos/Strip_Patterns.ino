void rainbow() {
    uint16_t pixel;
    uint16_t colourIncrement;
    uint16_t colour;
    const float NEXT_PIXEL = float(NUM_PIXELS) / 255.0;

    for( colour = 0; colour <= 255; colour++ ) {
        for( pixel = 0; pixel < NUM_PIXELS; pixel++ ) {
            colourIncrement = colour + round(NEXT_PIXEL * pixel);
            strip.setPixelColor(pixel, colourWheel(colourIncrement & 255));
            if( changePattern == true ) {
                delay(500);
                globalCount++;
                changePattern = false;
                return;
            }
        }
        strip.show();
        delay(20);
    }
}

void fillUp() {
    uint16_t filledPixel;
    uint16_t currPixel;
    uint16_t oppositePixel;
    uint8_t colour = random(0, 255);

    for( filledPixel = 0; filledPixel < (NUM_PIXELS / 2); filledPixel++ ) {
        for( currPixel = 0; currPixel < ((NUM_PIXELS / 2) - filledPixel); currPixel++ ) {
            oppositePixel = NUM_PIXELS - currPixel - 1;
            strip.setPixelColor(currPixel, colourWheel(colour));
            strip.setPixelColor(oppositePixel, colourWheel(colour));
            if( currPixel != 0 ) {
                strip.setPixelColor(currPixel - 1, 0);
                strip.setPixelColor(oppositePixel + 1, 0);
            }
            strip.show();
            if( changePattern == true ) {
                delay(500);
                globalCount++;
                changePattern = false;
                return;
            }
        }
        strip.show();
        colour += 1;
        colour = colour & 255;
    }

}

void colourSpin() {
    int16_t pixel;
    byte colours[NUM_PIXELS];
    
    for( pixel = 0; pixel < NUM_PIXELS; pixel++ ) {
        colours[pixel] = random(0, 255);
        strip.setPixelColor(pixel, colourWheel(colours[pixel]));
    }
    strip.show();

    uint32_t initialTime = millis();
    uint32_t durationForward = random(5000, 15000);
    uint32_t durationReverse = random(5000, 15000);
    while(true) {
        if( (initialTime + durationForward) > millis() ) {
            for( pixel = 0; pixel < NUM_PIXELS; pixel++ ) {
                if( pixel != 0 ) {
                    strip.setPixelColor(pixel-1, colourWheel(colours[pixel]));
                }
                else {
                    strip.setPixelColor((NUM_PIXELS-1), colourWheel(colours[0]));
                }
            }
            for( pixel = 0; pixel < NUM_PIXELS; pixel++ ) {
                if( pixel != 0 ) {
                    colours[pixel-1] = colours[pixel]; 
                }
                else {
                    colours[NUM_PIXELS-1] = colours[0];
                }
            }
        }  
        else if( (initialTime + durationForward + durationReverse) > millis() ) {
            for( pixel = 0; pixel < (NUM_PIXELS-1); pixel++ ) {
                if( pixel != (NUM_PIXELS-1) ) {
                    strip.setPixelColor(pixel+1, colourWheel(colours[pixel]));
                }
                else {
                    strip.setPixelColor(0, colourWheel(colours[NUM_PIXELS-1]));
                }
            }
            for( pixel = (NUM_PIXELS-1); pixel >= 0; pixel-- ) {
                if( pixel != (NUM_PIXELS-1) ) {
                    colours[pixel+1] = colours[pixel];
                }
                else {
                    colours[0] = colours[NUM_PIXELS-1];
                }
            }
        }
        else {
            initialTime = millis();
            durationForward = random(5000, 15000);
            durationReverse = random(5000, 15000);
        }
            strip.show();
            delay(50);
            if( changePattern == true ) {
                delay(500);
                globalCount++;
                changePattern = false;
                return;
            }
    }
        
}
