import os
import sys
os.chdir(os.getcwd() + '/..')
sys.path.append(os.getcwd())

import threading
import requests
import time
from config import Config

config = Config()

try:
    # Python 2.x
    from SocketServer import ThreadingMixIn
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
except ImportError:
    # Python 3.x
    from socketserver import ThreadingMixIn
    from http.server import BaseHTTPRequestHandler, HTTPServer


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


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
    r = requests.get(config.HTTP_SERVER_URL())
    print(r.content)


if __name__ == '__main__':
    server = ThreadingSimpleServer((config.HTTP_SERVER_ADRESS, config.HTTP_SERVER_PORT), Handler)
    st = threading.Thread(target=server.serve_forever)
    st.daemon = False
    st.start()

    start_time = time.time()
    t1 = threading.Thread(target=make_request)
    t1.start()
    t1.join()
    print(time.time() - start_time)

    #server.server_close()