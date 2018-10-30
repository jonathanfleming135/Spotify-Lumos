#!/usr/bin/python

import webbrowser
import time
import socket
import subprocess
import re
import datetime


id_file = open("client_id.txt", "r")
id_str = id_file.read()
id_file.close()

client_id, client_secret = id_str.split(",")



local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_socket.bind(('127.0.0.1', 8080))
local_socket.listen()

html_f = open("you_are_now_connected.html", 'r')
html = html_f.read()
html_f.close()

url_params = {
	"auth_url": "https://accounts.spotify.com/authorize/",
	"client_id":  "client_id={0}".format(client_id),
	"redirect": "redirect_uri=http://127.0.0.1:8080",
	"response": "response_type=code"
}

url = url_params["auth_url"]
url += "?" + url_params["client_id"]
url += "&" + url_params["redirect"]
url += "&" + url_params["response"]

webbrowser.open_new_tab(url)

res_params = {
	"HTTP": "HTTP/1.1 200 OK\n",
	"Date": "Date: {0}\n".format(str(datetime.datetime.now())),#Wed, 11 Apr 2012 21:29:04 GMT\n",#{0}\n".format(str(datetime.datetime.now())),
	"Server": "Server: Python/6.6.6 (custom)\n",
	"Connection": "Connection: closed\n",
	"Content-Type": "Content-Type: text/html \n\n",
	"html": "<html>\n{0}</html>".format(html)
}

response = ""
response += res_params["HTTP"]
response += res_params["Date"]
response += res_params["Server"]
response += res_params["Connection"]
response += res_params["Content-Type"]
response += res_params["html"]


connection, addr = local_socket.accept()
while True:
	data = connection.recv(1024)
	if (data):
		print(data)
		connection.send(response.encode())
		local_socket.close()
		connection.close()
		break

regex = re.search('code=(\S+)', data.decode())
token = regex.group(1)

token_file = open("../../metadata/token.txt", "w+")
token_file.write(token)
token_file.close()

# may not be necessary since sshfs
#bashCommand = "scp {0} lumos:~/spotify-lumos/metadata"
