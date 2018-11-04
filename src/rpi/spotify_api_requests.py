#!/usr/bin/python

import requests
import time

# get the access token
access_token_file = open("../../metadata/access_token.txt", "r")
token = access_token_file.read()
access_token_file.close()

# constants
get_current_song_endpoint =  "https://api.spotify.com/v1/me/player/currently-playing"
get_song_analysis_endpoint = "https://api.spotify.com/v1/audio-analysis/"
get_song_features_endpoint = "https://api.spotify.com/v1/audio-features/"

def get_currently_playing_song():
	'''
	This method will be used like a "private" method for this file,
	it should not be called by methods outside this file
	'''

	params = {
		"Authorization": "Bearer {0}".format(token)
	}

	req = requests.get(get_current_song_endpoint, headers=params)
	print(req.text)

def get_song_features(song_uri):
	pass

def get_song_analysis(song_uri):
	pass

get_currently_playing_song()