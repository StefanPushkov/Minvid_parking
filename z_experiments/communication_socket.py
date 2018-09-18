import socket
import json
from threading import Thread

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 19701

class SocketManager:
    def __init__(self, json_callback):
        self.json_callback = json_callback
        self.socket = socket.socket()
        self._start()

    def _start(self):
        self.is_active = True
        self.socket.bind((SERVER_ADDRESS, SERVER_PORT))
        self.socket.listen(10) #length of queue
        Thread(target=self._loop).start()


    def stop(self):
        self.is_active = False

        client = socket.socket()
        client.settimeout(0.1)
        client.connect((SERVER_ADDRESS, SERVER_PORT))
        client.send('-1'.encode())
        client.close()

    def _loop(self):
        while self.is_active:
            conn, addr = self.socket.accept()
            camera_ip_bytes = conn.recv(4096)
            camera_ip = int(camera_ip_bytes.decode('utf8'))
            if camera_ip == -1:
                conn.send(b'')
            else:
                conn.send(self.json_callback(camera_ip).encode('utf8'))
            conn.close()

def get_json_from_request(camera_ip):
    json_obj = None
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.settimeout(8.0)
        client.connect((SERVER_ADDRESS, SERVER_PORT))

        client.send(str.encode(camera_ip))
        json_bytes = client.recv(4096)

        json_string = json_bytes.decode('utf8')
        json_obj = json.loads(json_string)

        client.shutdown(socket.SHUT_RDWR)
        client.close()
    except Exception as msg:
        json_obj = {
            'status': -3,
            'error': msg
        }
    return json_obj


if __name__ == "__main__":
    def json_callback(camera_ip):
        return '{"camera_ip_bytes":"' + str(camera_ip) + '"}'

    sockMan = SocketManager(json_callback)

    import time
    time.sleep(1)

    print(get_json_from_request('1'))

    sockMan.stop()