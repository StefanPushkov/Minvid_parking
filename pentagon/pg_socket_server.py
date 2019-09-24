# Implementation of socket server.
# Should work at the same machine as its client
# Allows multiple connections, max number specified in config


import socket
from threading import Thread
import time

import configs.pentagon as config


class PGSocketServer:
    def __init__(self, callback):
        self.is_active = False
        self.threads_max = config.SOCKET_MAX_THREADS
        self.threads_count = 0

        self.make_shot_and_get_json_string = callback
        self.socket = socket.socket()
        self._start()

    def _start(self):
        self.is_active = True
        self.socket.bind((config.SOCKET_SERVER_ADDRESS, config.SOCKET_SERVER_PORT))
        self.socket.listen(10)  # length of queue
        Thread(target=self._loop).start()

    def stop(self):
        self.is_active = False
        self.socket.close()

    def _loop(self):
        while self.is_active:
            if self.threads_count < self.threads_max:
                t = Thread(target=self._process_request)
                t.start()

            time.sleep(0.01)

    def _process_request(self):
        self.threads_count += 1

        conn, addr = self.socket.accept()

        camera_ip_bytes = conn.recv(4096)
        camera_ip = camera_ip_bytes.decode('utf8')

        json_string = self.make_shot_and_get_json_string(camera_ip)
        json_bytes = json_string.encode('utf8')
        conn.send(json_bytes)

        conn.close()

        self.threads_count -= 1
