# Spotify Lumos
An RGB LED strip that synchronizes with music playing from Spotify!

[Sample Video](https://youtu.be/Ehpbet-ZupI)

## Background/Summary
The idea behind this project is to get a fully addressable RGB LED strip to automatically synchronize to whatever song is currently playing on spotify. It is a personal project I have been working for fun and coding practice. A user should be able to simply connect to spotify-lumos through a mobile device and then play songs normally on spotify to get it to work!

## Progress
The "minimum viable product" version of this project is complete. Currently I am able to connect to the spotify-lumos Raspberry Pi via my phone and play songs through spotify. The system then detects a song is being played, and lights up the LEDs accordingly. Currently, only one pattern exists and changes the number of LEDs lit up based on volume, along with colour based on pitch.

## Goal
The goal of this project is to create an LED strip that synchronizes with music playing from Spotify. Ideally, it should contain the following features/functionality:
- Require minimal user effort to turn on and off once everything is installed. 
- Work in any room with a square or rectangular ceiling. 
- Contain multiple patterns that automatically sync with the current music playing from Spotify 
- Respond to changes in the music player appropriately (pauses when the song pauses, synchronizes with a new song shortly after a user changes songs, etc).
- Recognize different sections of a song (chorus, bridge, etc) along with properties of the song (danceability, intensity, etc) and select patterns accordingly. 
- Finally, everything should work together reasonably well (there should not be any major bugs).

## How it works
Here, I will explain the system from the bottom up. The LED strip is powered from an external power source and directly controlled from the GPIO pins from an Arduino Uno. The Arduino uses the [Adafruit NeoPixel Library](https://github.com/adafruit/Adafruit_NeoPixel) to control the LEDs. The Arduino itself is controlled from the Raspberry Pi via a UART connection.

The Raspberry Pi controls the Arduino by sending "packets" of data over the UART connection. The data tells the Arduino which LEDs to light up and what colour to use. The Arduino then lights up these LEDs and waits until the next packet is received from the Raspberry Pi. Essentially, this is all the Arduino is used for, as the Raspberry Pi was unable to control the LED strip while playing music on a speaker connected through its AUX port.

The Raspberry Pi has multiple jobs, only one of which is to send data to the Arduino. The Raspberry Pi also acts as a Spotify server, which allows it to connect to devices on the same network that have the Spotify application. This also allows it to play music on a speaker connected through its AUX port. This is done using [Raspotify](https://dtcooper.github.io/raspotify).

Furthermore, the Raspberry Pi is responsible for making requests to Spotify web API's to get info about the user's currently playing song. From this data, the Raspberry Pi creates patterns to light up the LEDs in a way that "visualizes" the music. This is done in python is still a work in progress.
