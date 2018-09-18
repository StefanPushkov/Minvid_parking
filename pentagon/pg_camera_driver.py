# Client that requests ip camera for image


import cv2
import numpy as np
import requests
import time

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

    def generate_image_path(self):
        #TODO add realization!!!
        pass


    def make_shot(self, camera_ip):
        self.auth()
        r = requests.get('http://192.168.60.9/scapture',
                         headers={'Connection': 'keep-alive', 'Cookie': self.cookie})

        array = np.frombuffer(r.content, dtype=np.uint8)
        image = cv2.imdecode(array, cv2.IMREAD_GRAYSCALE)

        path = self.generate_image_path()
        cv2.imwrite(path, image)

        return image, path