import os
import sys
os.chdir(os.getcwd() + '/..')
sys.path.append(os.getcwd())

import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

from config import CONFIG


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(str(self.address_string), 'utf8'))
        return

    def do_POST(self):
        # Begin the response
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        print(self.data_string)
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        print('post---------')
        return

def make_request():
    r = requests.get(CONFIG.HTTP_SERVER_URL())
    print(r.content)


if __name__ == '__main__':
    server = HTTPServer((CONFIG.HTTP_SERVER_ADRESS, CONFIG.HTTP_SERVER_PORT), Handler)
    st = threading.Thread(target=server.serve_forever)
    st.daemon = True
    st.start()

    make_request()

    #server.server_close()