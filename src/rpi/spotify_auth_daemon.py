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

print(req.text)