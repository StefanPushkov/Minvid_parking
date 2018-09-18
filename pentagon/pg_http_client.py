# Client that makes request to a production server


import requests
import cv2
from json import dumps

from config import Config
config = Config()

def make_request(image):
    image = cv2.imread('/media/data/server_img/analyze/152386286686123_full.png', 0)

    files = {'shape': str(dumps(image.shape)), 'image': image.tobytes()}

    r = requests.post(config.HTTP_SERVER_URL(), headers={'Content-Type': 'image/gif'}, files=files)

    return r.json()