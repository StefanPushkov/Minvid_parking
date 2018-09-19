# This is the daemon for image grabbing service placed on object pc.
# When requested, takes image from ip camera, saves it to disk,
# makes request to computational service (http, user data is json encrypted with AES),
# finally returns json with path to image and result of recognition


import os
import sys
os.chdir(os.getcwd() + '/..')
sys.path.append(os.getcwd())

import time
from pentagon.pg_socket_server import PGSocketServer
from pentagon.pg_camera_driver import PGCameraDriver
from pentagon.pg_http_client import make_request
import json

class PGMain:
    def __init__(self):
        self.camera_driver = PGCameraDriver()
        self.server = PGSocketServer(self.make_shot_and_get_json_string)

    def stop(self):
        self.server.stop()

    def make_shot_and_get_json_string(self, shot_path):
        image, path = self.camera_driver.get_image_by_ip_and_save(shot_path)

        json_obj = make_request(image)
        json_obj['plate'] = ''
        json_obj['image'] = shot_path

        return json.dumps(json_obj)

    def save_plate_image(self, image, frame):
        pass



if __name__ == '__main__':
    PGMain()

    while 1:
        time.sleep(1)