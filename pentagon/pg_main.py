""" This is the daemon for image grabbing service placed on object pc.
When requested, takes image from ip camera, saves it to disk,
makes request to computational service (http, user data is json encrypted with AES),
finally returns json with path to image and result of recognition"""

import json
import os
import sys
import time
from threading import Thread
import logging

from pg_socket_server import PGSocketServer
from pg_camera_driver import PGCameraDriver
from pg_moxa_driver import PGMoxaDriver
from pg_http_client import make_request

import configs.pentagon as config


base_dir = config.get_base_dir_by_name('carplates_server')
sys.path.append(base_dir)


class PGMain:
    def __init__(self):
        self.camera_driver = PGCameraDriver()
        # self.server = PGSocketServer(self.make_shots_and_get_plate)
        self.moxa = PGMoxaDriver(self.on_car_detected)

    # def stop(self):
        # self.server.stop()

    def on_car_detected(self, camera_ip: str):
        Thread(target=lambda: self.on_car_detected_t(camera_ip)).start()

    def on_car_detected_t(self, camera_ip: str):
        plate = self.make_shots_and_get_plate(camera_ip)

        if plate:
            logging.info('Recognition done! Plate: ' + plate)
        else:
            logging.error('Recognition error! Check Godfather logs for details.')

    def make_shots_and_get_plate(self, camera_ip):
        plate = None
        for i in range(0, config.PHOTO_SERIES_SIZE):
            image = self.camera_driver.get_image_by_ip(camera_ip)

            if image is None:
                json_obj = {'status': -2,
                            'error': 'Error communicating with camera'}
                return json.dumps(json_obj)

            if i == config.PHOTO_SERIES_SIZE - 1:
                plate = make_request(image, is_last=True)
            else:
                make_request(image)
                time.sleep(config.SHOT_INTERVAL / 1000)

        return plate


if __name__ == '__main__':
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    fh = logging.FileHandler(config.LOG_FILE)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler(sys.stdout)

    logging.basicConfig(level=config.LOG_LEVEL, handlers=[ch, fh])

    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

    PGMain()

    while 1:
        time.sleep(1)
