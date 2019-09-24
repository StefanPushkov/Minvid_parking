# This is the multithreaded http server implementation

import base64
import json

from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer

import configs.godfather as config

from aes_cipher import AESCipher

cipher = AESCipher(config.AES_PASSPHRASE)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class GFHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        data_bytes = self.rfile.read(int(self.headers['Content-Length']))
        body = cipher.decrypt(data_bytes)

        json_request = json.loads(body)

        cookie = json_request['cookie']

        image = json_request['image'].encode('utf-8')
        image = base64.b64decode(image)

        if cookie != config.HTTP_COOKIE:
            self.send_response(401)  # 401 Unauthorized
            self.end_headers()
            self.wfile.write(b'{"error":"Unknown user!"}')
            return

        encr_response = ''

        self.server.alpr.predict(image)
        if 'last_image' in json_request and json_request['last_image']:
            results = list()
            self.server.alpr.block_until_done()
            for result in self.server.alpr.get_results():
                results.append(result)
            results = list(filter(lambda a: a is not None, results))
            answer = max(set(results), key=results.count)
            if config.ENABLE_DB:
                self.server.db.add_shot(answer, image)

            response = json.dumps({'cookie': config.HTTP_COOKIE, 'plate': answer})
            encr_response = cipher.encrypt(response)

        self.send_response(200)
        self.end_headers()
        if type(encr_response) == bytes:
            self.wfile.write(bytes(encr_response))
        else:
            self.wfile.write(bytes(encr_response, 'utf-8'))
        return
