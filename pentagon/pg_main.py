# This is the daemon for image grabbing service placed on object pc.
# When requested, takes image from ip camera, saves it to disk,
# makes request to computational service (http, user data is json encrypted with AES),
# finally returns json with path to image and result of recognition


import os
import sys
# gets path of project directory
def get_base_dir_by_name(name):
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]
base_dir = get_base_dir_by_name('carplates_server')
sys.path.append(base_dir)

import time
from threading import Thread
import logging

from pentagon.pg_socket_server import PGSocketServer
from pentagon.pg_camera_driver import PGCameraDriver
from pentagon.pg_moxa_driver import PGMoxaDriver
from pentagon.pg_database import Database
from pentagon.pg_http_client import make_request
import json

from config import CONFIG

logger = logging.getLogger(__name__)
logger.setLevel(CONFIG.PG_MAIN_LOGGER_LEVEL)

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

        if json_obj['status'] == 1:
            logger.info('RECOGNITION DONE, saving to db')
            self.db.add_shot(json_obj)
        else:
            logger.warning('Answer has error status! answer: ' + json.dumps(json_obj))


    def make_shot_and_get_json_string(self, camera_ip):
        image, path = self.camera_driver.get_image_by_ip_and_save(camera_ip)

        if image is None:
            json_obj = {'status': -2,
                        'error': 'Error communicating with camera'}
            return json.dumps(json_obj)

        json_obj = make_request(image)

        if json_obj is None:
            json_obj = {'status': -1,
                        'error': 'Error communicating with Sekkar Engine'}
            return json.dumps(json_obj)

        json_obj['plate'] = ''
        json_obj['image'] = path

        return json.dumps(json_obj)



if __name__ == '__main__':
    import logging
    fh = logging.FileHandler(CONFIG.PROJECT_DIR + '/pg_main.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.DEBUG, handlers=[ch, fh])
    logging.critical('START SERVER')
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

    PGMain()

    while 1:
        time.sleep(1)