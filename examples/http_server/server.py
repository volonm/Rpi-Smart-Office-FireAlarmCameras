from http.server import BaseHTTPRequestHandler, HTTPServer
from json import JSONDecoder, JSONEncoder
from os import read


class RequestHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        data = JSONEncoder().encode({"ALARM": 2}).encode()

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        print("DATA: ", JSONDecoder().decode(self.rfile.read().decode()))
        self.send_response(201)

address = ("0.0.0.0", 5000)
server = HTTPServer(address, RequestHandler)
print("Running on: ", address)

try:
    server.serve_forever()
except:
    print("Bye")