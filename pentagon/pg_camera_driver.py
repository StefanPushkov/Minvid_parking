# Client that requests ip camera for image


import cv2
import numpy as np
import requests
import datetime
import os

from config import CONFIG

class PGCameraDriver:

    cookie = None

    def auth(self, camera_ip):
        url = 'http://' + camera_ip + '/login.html' # camera_ip example: 192.168.60.9
        r = requests.post(url,
                          data={'p_send': '1', 'p_username': 'admin', 'p_passw': 'Sinergija777'},
                          headers={'Connection': 'keep-alive'})

        raw_cookie = r.headers['Set-Cookie']
        # raw_cookie: GXSU=NYyVwylzcdFJOT9; Path=/; Expires=Sun, 09-Sep-2018 15:12:06 GMT; Max-Age=1800; HttpOnly

        cookie_str = raw_cookie[:raw_cookie.find(';')]
        # cookie_str: GXSU=NYyVwylzcdFJOT9
        self.cookie = cookie_str

    @staticmethod
    def generate_image_path():
        path = CONFIG.images_root_folder

        now = datetime.datetime.now()

        # filename = 'image_15_07_17_733178.png'
        filename = 'image_' + \
                   str(now.time()).replace('.', '_').replace(':', '_') +\
                   '.png'

        path = os.path.join(path,
                            str(now.year),
                            str(now.month),
                            str(now.day),
                            filename)

        return path


    def get_image_by_ip_and_save(self, camera_ip):
        self.auth()

        url = 'http://' + camera_ip + '/scapture'  # example: http://192.168.60.9/scapture
        r = requests.get(url,
                         headers={'Connection': 'keep-alive', 'Cookie': self.cookie})

        array = np.frombuffer(r.content, dtype=np.uint8)
        image = cv2.imdecode(array, cv2.IMREAD_GRAYSCALE)

        path = self.generate_image_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cv2.imwrite(path, image)

        return image, path