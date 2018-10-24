#!/usr/bin/python

import requests
import webbrowser
import time
import socket
import http.server
import socketserver

id_file = open("../client_id.txt", "r")
id_str = id_file.read(1000)
id_file.close()

client_id, client_secret = id_str.split(",")
print(client_id)

#local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#local_socket.bind(('127.0.0.1', 8080))
#local_socket.listen()

parameters = {
	#"response_type": "code",
	#"redirect_uri": "http://127.0.0.1/callback:8080",
	"client_id": str(client_id)
}

#parameters = {
#	"client_id": str(client_id)
#}

html = '<h1><span style="color: #ff0000;">You</span> <span style="color: #ff6600;">are</span> <span style="color: #ffff00;">now</span> <span style="color: #339966;">connected</span> <span style="color: #0000ff;">to</span> <span style="color: #333399;">spotify</span>-<span style="color: #993366;">lumos</span>!</h1><p>&nbsp;</p>'

# class myHandler (http.server):
# 	def do_GET(self):
# 		self.send_response(200)
# 		self.send_header('Content-type','text/html')
# 		self.end_headers()
# 		self.wfile.write(html)
# 		return

# https://accounts.spotify.com/authorize/?client_id=fa731c70a97a467cba0096e77092dad4&redirect_uri=http://127.0.0.1/callback:8080&response_type=code
#url = "https://accounts.spotify.com/authorize/?client_id=fa731c70a97a467cba0096e77092dad4&redirect_uri=https://jonathanfleming135.github.io/Spotify-Lumos/&response_type=code"
url = "https://accounts.spotify.com/authorize/?client_id=fa731c70a97a467cba0096e77092dad4&redirect_uri=http://127.0.0.1:8080&response_type=code"
chrome_path = "/usr/bin/google-chrome"
webbrowser.get(chrome_path).open(url)


# Handler = http.server.SimpleHTTPRequestHandler("/home/jon/tmp")

# with socketserver.TCPServer(("127.0.0.1", 8080), Handler) as httpd:
# 	httpd.handle_request()


# python -m http.server 8000 --bind 127.0.0.1
# python -m http.server --directory /tmp/

'''
connection, addr = local_socket.accept()
while True:
	data = connection.recv(1024)
	if (data):
		print(data)
		connection.send(response)
'''


#time.sleep(10)

#resp = requests.get("https://jonathanfleming135.github.io/Spotify-Lumos/")
#print(resp.content)

#response = requests.post("https://accounts.spotify.com/authorize/?client_id=fa731c70a97a467cba0096e77092dad4&redirect_uri=https://jonathanfleming135.github.io/Spotify-Lumos/&response_type=code", timeout=60.0)

#print(response.status_code)

#print(response.content)


#"https://jonathanfleming135.github.io/Spotify-Lumos/"
