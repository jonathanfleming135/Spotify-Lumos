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

# song timing
curr_song_end_time = -1.0
uri = ""
song_change = False

# song analysis and features
song_features = {}
song_analysis = {}
features_change = False
analysis_change = False

def get_currently_playing_song():
	'''
	This method will be used like a "private" method for this file,
	it should not be called by methods outside this file.

	All times expressed in seconds expressed as a float

	returns the uri of the song being currently played
	'''

	global token
	global curr_song_end_time
	global uri
	global song_change

	if (time.clock() < curr_song_end_time and not song_change):
		return uri
	else:
		headers = {
			"Authorization": "Bearer {0}".format(token)
		}

		req = requests.get(get_current_song_endpoint, headers=headers)
		req = req.json()

		progress = float(req["progress_ms"]) / 1000.0
		duration = float(req["item"]["duration_ms"]) / 1000.0
		curr_song_end_time = (duration - progress) + time.clock()
		song_change = False

		uri = req["item"]["uri"].split(":")[-1]
		return uri

def check_currently_playing_song():
	'''
	This method should be called every 3 seconds - to check the currently
	playing song hasn't changed (in the case a user manually selects a
	different song)
	'''

	global token
	global uri
	global song_change
	global features_change
	global analysis_change

	headers = {
		"Authorization": "Bearer {0}".format(token)
	}

	req = requests.get(get_current_song_endpoint, headers=headers)
	req = req.json()


	curr_song_uri = req["item"]["uri"].split(":")[-1]
	if (uri != curr_song_uri):
		song_change = True
		features_change = True
		analysis_change = True
		uri = curr_song_uri
		#TODO - call method to recalculate patterns for a song

def get_song_features():
	'''
	This function returns a json object of the spotify song features
	api corresponding to the currently playing song

	It is meant to be called anywhere in the code
	'''

	global token
	global uri
	global song_features
	global features_change

	prev_uri = uri
	curr_uri = get_currently_playing_song()

	if (curr_uri == prev_uri and not features_change):
		return song_features
	else:
		endpoint = "{0}{1}".format(get_song_features_endpoint, uri)

		headers = {
			"Authorization": "Bearer {0}".format(token)
		}

		req = requests.get(endpoint, headers=headers)
		req = req.json()

		features_change = False
		song_features = req
		return req


def get_song_analysis():
	'''
	This function returns a json object of the spotify song analysis
	api corresponding to the currently playing song

	It is meant to be called anywhere in the code
	'''
	global token
	global uri
	global song_analysis
	global analysis_change

	prev_uri = uri
	curr_uri = get_currently_playing_song()

	if (curr_uri == prev_uri and not analysis_change):
		return song_analysis
	else:
		endpoint = "{0}{1}".format(get_song_analysis_endpoint, uri)

		headers = {
			"Authorization": "Bearer {0}".format(token)
		}

		req = requests.get(endpoint, headers=headers)
		req = req.json()

		analysis_change = False
		song_analysis = req
		return req