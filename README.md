# Spotify Lumos
An RGB LED strip that synchronizes with music playing from Spotify!

## Background/Summary
The idea behind this project is to get a fully addressable RGB LED strip to automatically synchronize to whatever song is currently playing on spotify. It is a personal project I have been working for fun and coding practice. A user should be able to simply connect to spotify-lumos through a mobile device and then play songs normally on spotify to get it to work!

## Progress
Currently, the "minimum viable product" version of this project is complete. Currently I am able to connect to the spotify-lumos Raspberry Pi via my phone and play songs through spotify. The strip then detects a song is being played, and lights up the LEDs accordingly. Currently, only one pattern exists and changes the number of LEDs lit up based on volume, along with colour based on pitch.

## Goal
The goal of this project is to create an LED strip that synchronizes with music playing from Spotify. Ideally, it should contain the following features/functionality:
- Require minimal user effort to turn on and off once everything is installed. 
- Work in any room with a square or rectangular ceiling. 
- Contain multiple patterns that automatically sync with the current music playing from Spotify 
- Respond to changes in the music player appropriately (pauses when the song pauses, synchronizes with a new song shortly after a user changes songs, etc).
- Recognize different sections of a song (chorus, bridge, etc) along with properties of the song (danceability, intensity, etc) and select patterns accordingly. 
- Finally, everything should work together reasonably well (there should not be any major bugs).

## How it works


Uses Raspotify:
Raspotify - Spotify Connect client for the Raspberry Pi that Just Works™ https://dtcooper.github.io/raspotify 
Summary
