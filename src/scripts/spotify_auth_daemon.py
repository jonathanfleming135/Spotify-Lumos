#!/usr/bin/python

import time
import requests

id_file = open("../../metadata/client_id.txt", "r")
id_str = id_file.read()
id_file.close()
client_id, client_secret = id_str.split(",")

token_file = open("../../metadata/token.txt", "r")
code = token_file.read()
token_file.close()

params = {
	"grant_type": "authorization_code",
	"code": str(code),
	"redirect_uri": "http://127.0.0.1:8080",
	"client_id": str(client_id),
	"client_secret": str(client_secret)
}

req = requests.post("https://accounts.spotify.com/api/token", data=params)
response = req.json()

access_token = 	response["access_token"]
refresh_token = response["refresh_token"]
expires_in = 	response["expires_in"]

access_token_file = open("../../metadata/access_token.txt", "w+")
access_token_file.write(access_token)
access_token_file.close()

while (True):
	time.sleep(expires_in - 60)

	refresh_params = {
		"grant_type": "refresh_token",
		"refresh_token": refresh_token,
		"client_id": str(client_id),
		"client_secret": str(client_secret)
	}

	req = requests.post("https://accounts.spotify.com/api/token", data=refresh_params)
	response = req.json()

	expires_in = 	response["expires_in"]
	access_token = 	response["access_token"]

	access_token_file = open("../../metadata/access_token.txt", "w+")
	access_token_file.write(access_token)
	access_token_file.close()