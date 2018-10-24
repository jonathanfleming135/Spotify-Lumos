#!/usr/bin/python

import webbrowser
import time
import socket
import re

'''
id_file = open("../rpi/client_id.txt", "r")
id_str = id_file.read(1000)
id_file.close()

client_id, client_secret = id_str.split(",")
print(client_id)
'''

local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_socket.bind(('127.0.0.1', 8080))
local_socket.listen()

html = '<h1><span style="color: #ff0000;">You</span> <span style="color: #ff6600;">are</span> <span style="color: #ffff00;">now</span> <span style="color: #339966;">connected</span> <span style="color: #0000ff;">to</span> <span style="color: #333399;">spotify</span>-<span style="color: #993366;">lumos</span>!</h1><p>&nbsp;</p>'

url = "https://accounts.spotify.com/authorize/?client_id=fa731c70a97a467cba0096e77092dad4&redirect_uri=http://127.0.0.1:8080&response_type=code"
chrome_path = "/usr/bin/google-chrome"
webbrowser.open_new_tab(url)



response = '''
HTTP/1.1 200 OK
Date: Wed, 11 Apr 2012 21:29:04 GMT
Server: Python/6.6.6 (custom)
Connection: closed
Content-Type: text/html \n
<html>
<h1><span style="color: #ff0000;">You</span> <span style="color: #ff6600;">are</span> <span style="color: #f4d03f;">now</span> <span style="color: #4cd900;">connected</span> <span style="color: #0000ff;">to</span> <span style="color: #333399;">spotify</span>-<span style="color: #993366;">lumos</span>!</h1><p>&nbsp;</p>
</html>
'''


connection, addr = local_socket.accept()
while True:
	data = connection.recv(1024)
	if (data):
		print(data)
		connection.send(response.encode())
		local_socket.close()
		break

regex = re.search('code=(\S+)', data.decode())
print(regex.group(1))