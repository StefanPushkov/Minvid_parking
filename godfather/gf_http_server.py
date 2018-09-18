# This is the multithreaded http server implementation


from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
import json

from config import CONFIG

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
        data_bytes = self.rfile.read(int(self.headers['Content-Length']))
        # first 200 bytes of data_bytes:
        #
        # b'--24f1c846973f90d95eff87e2ebc2598b\r\n
        # Content-Disposition: form-data; name="data"; filename="data"\r\n
        # \r\n
        # {"shape": [480, 752], "cookie": "KfFdxguMgver6kI"}\n
        # HP_mqnlnggn|\x84\x82|x~wnea`absiemvz~\x83\x88\x87\x80|\x86\x95\x96\x8d\x86\x8c\x8c\x8a\x92\xa1\xa4\x9d\x9c'
        #
        #
        # structure: start_http_default - \r\n - json - \n - image_as_bytes - end_http_default(40bytes)

        data_bytes = data_bytes[:-40]  # cut end_http_default

        #cut start_http_default:
        for i in range(3):
            index = smart_index(data_bytes, b'\n') + 1
            data_bytes = data_bytes[index:]

        index = smart_index(data_bytes, b'\n') + 1
        json_bytes = data_bytes[:index-1]
        image_bytes = data_bytes[index:]

        json_string = json_bytes.decode("ascii")
        json_object = json.loads(json_string)

        if json_object["cookie"] != CONFIG.HTTP_COOKIE:
            self.send_response(401)  # 401 Unauthorized
            self.end_headers()
            self.wfile.write(b'{"error":"Unknown user!"}')
            return

        image = np.frombuffer(image_bytes, dtype=np.uint8)
        image = image.reshape(json_object["shape"])

        answer = self.server.predict(image)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(answer, 'utf8'))
        return