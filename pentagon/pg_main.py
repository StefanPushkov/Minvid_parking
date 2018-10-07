# This is the daemon for image grabbing service placed on object pc.
# When requested, takes image from ip camera, saves it to disk,
# makes request to computational service (http, user data is json encrypted with AES),
# finally returns json with path to image and result of recognition


import os
import sys

if __name__ == '__main__':
    os.chdir(os.getcwd() + '/..')
    sys.path.append(os.getcwd())

import time
from threading import Thread

from pentagon.pg_socket_server import PGSocketServer
from pentagon.pg_camera_driver import PGCameraDriver
from pentagon.pg_moxa_driver import PGMoxaDriver
from pentagon.pg_database import Database
from pentagon.pg_http_client import make_request
import json

class PGMain:
    def __init__(self):
        self.camera_driver = PGCameraDriver()
        self.server = PGSocketServer(self.make_shot_and_get_json_string)
        self.moxa = PGMoxaDriver(self.on_car_detected)
        self.db = Database()

    def stop(self):
        self.server.stop()

    def on_car_detected(self, camera_ip: str):
        Thread(target= lambda : self.on_car_detected_t(camera_ip)).start()

    def on_car_detected_t(self, camera_ip:str):
        json_str = self.make_shot_and_get_json_string(camera_ip)
        json_obj = json.loads(json_str)
        self.db.add_shot(json_obj)

    def make_shot_and_get_json_string(self, camera_ip):
        image, path = self.camera_driver.get_image_by_ip_and_save(camera_ip)

        json_obj = make_request(image)
        json_obj['plate'] = ''
        json_obj['image'] = path

        return json.dumps(json_obj)

    def save_plate_image(self, image, frame):
        pass



if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)

    PGMain()

    while 1:
        time.sleep(1)