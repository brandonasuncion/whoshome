#!/usr/bin/env python3
import http.server
import whoshome

HOST_NAME = ''
PORT_NUMBER = 8080


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(404)
            return

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        #self.wfile.write(b"WHO'S HOME\n")

        for user in whoshome.activeUsers():
            self.wfile.write("{}\n".format(user).encode())

if __name__ == '__main__':
    server = http.server.HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()