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
import cv2

from trucks_weight.tw_filesystem_utils import find_files_added_in_last_5_sec, copy_image_with_recog_in_name
from trucks_weight.tw_http_client import make_request

from config import CONFIG

logger = logging.getLogger(__name__)
logger.setLevel(CONFIG.PG_MAIN_LOGGER_LEVEL)

class PGMain:
    already_recognized_images_paths = []

    def __init__(self):
        self.is_active = True
        Thread(target=self._loop).start()

    def stop(self):
        self.is_active = False

    def _loop(self):
        while(self.is_active):
            time.sleep(1)

            #prevent list from becoming too big
            # (it wouid fail if 50+ photos would be done in 5 seconds, but the chances are too small)
            if len(self.already_recognized_images_paths) > 100:
                before = len(self.already_recognized_images_paths)
                self.already_recognized_images_paths = self.already_recognized_images_paths[50:]
                after = len(self.already_recognized_images_paths)
                logger.debug("Make already_recognized_images_paths list shorter. Before: %d, after: %d"
                             % (before, after))

            new_files:list = find_files_added_in_last_5_sec()
            for new_file in new_files:
                if new_file in self.already_recognized_images_paths:
                    logger.debug("already recognized: " + new_file)
                    continue
                else:
                    logger.debug("found new file: " + new_file)

                self.already_recognized_images_paths.append(new_file)
                Thread(target=lambda: self.process_recognition_t(new_file)).start()

    def process_recognition_t(self, path:str):
        number = self.make_request_for_plate_number(path)

        if number is None:
            logger.warning('Failed to process recognition!')
            return

        copy_image_with_recog_in_name(path, number)


    def make_request_for_plate_number(self, path):
        image = cv2.imread(path, 0)

        if image is None:
            logger.warning("Cannot make request: image is None")
            return None

        json_obj = make_request(image)

        if json_obj is None:
            return None

        try:
            return json_obj['number']
        except Exception as e:
            logger.warning("got exception: " + str(e))
            return None



if __name__ == '__main__':
    import logging
    fh = logging.FileHandler(CONFIG.PROJECT_DIR + '/tw_main.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.DEBUG, handlers=[ch, fh])
    logging.critical('START SERVER')
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

    PGMain()

    while 1:
        time.sleep(1)