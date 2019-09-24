# Client that requests ip camera for image


import requests
import datetime
import os
import logging

import configs.pentagon as config


class PGCameraDriver:

    cookie = None

    def auth(self, camera_ip) -> bool:
        url = 'http://' + camera_ip + '/login.html'
        try:
            r = requests.post(url,
                              data={'p_send': '1', 'p_username': 'admin', 'p_passw': 'Sinergija777'},
                              headers={'Connection': 'keep-alive'},
                              timeout=2)
        except Exception as e:
            logging.error('Error requesting camera with url %s, ERR: %s' % (url, str(e)))
            return False

        if 'Set-Cookie' not in r.headers:
            logging.warning('No Set-Cookie in headers!')
            return False

        raw_cookie = r.headers['Set-Cookie']
        # raw_cookie: GXSU=NYyVwylzcdFJOT9; Path=/; Expires=Sun, 09-Sep-2018 15:12:06 GMT; Max-Age=1800; HttpOnly

        cookie_str = raw_cookie[:raw_cookie.find(';')]
        # cookie_str: GXSU=NYyVwylzcdFJOT9
        self.cookie = cookie_str
        return True

    @staticmethod
    def generate_image_path():
        path = config.IMAGE_ROOT_FOLDER

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

    def get_image_by_ip(self, camera_ip):
        self.auth(camera_ip)

        url = 'http://' + camera_ip + '/scapture'  # example: http://192.168.60.9/scapture
        try:
            r = requests.get(url,
                             headers={'Connection': 'keep-alive', 'Cookie': self.cookie})
        except Exception as e:
            logging.error('Error requesting camera with url %s, ERR: %s' % (url, str(e)))
            return None, None

        image = r.content

        if image is None:
            logging.error('Error reading image from camera with url %s' % url)
            return None, None

        return image
