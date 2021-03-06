#!/usr/bin/env python
'''

A very simple Python webserver that isn't very good.

'''

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

sitedir = "." #could set to /var/www if your normal site is there, etc.

class RequestHandler(BaseHTTPRequestHandler):
	def _writeheaders(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_HEAD(self):
		self._writeheaders()

	def do_GET(self):
		self._writeheaders()
		
		if self.path == "/":
			self.path = "index.html"
		
		try:
			f = open(sitedir + self.path)
			self.wfile.write(f.read())
			f.close()
		except IOError, e: # probably means we tried fetching a directory
			self.wfile.write("Couldn't find file")
			print e

serveraddr = ('', 8080)
srvr = HTTPServer(serveraddr, RequestHandler)
 
print("Server online and active")
 
srvr.serve_forever()
