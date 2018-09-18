# This is the multithreaded http server implementation


from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
import json

# index that returns -1 instead of throwing ValueError
def smart_index(bytess, byte):
    index = -1
    try:
        index = bytess.index(byte)
    except ValueError:
        pass
    return index

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class GFHandler(BaseHTTPRequestHandler):

    # read image to np.array, predict -> get json answer, send answer
    def do_POST(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        for i in range(7):
            index = smart_index(data_string, b'\n') + 1
            data_string = data_string[index:]
            if i == 2:
                index2 = smart_index(data_string, b'\r')
                imshape = data_string[:index2]
                imshape = json.loads(imshape)
        index = smart_index(data_string, b'\r')
        data_string = data_string[:-40]

        image = np.frombuffer(data_string, dtype=np.uint8)
        image = image.reshape(imshape)

        answer = self.server.predict(image)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(answer, 'utf8'))
        return