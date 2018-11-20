# Client that makes request to a production server


import requests
import cv2
import json
import logging

from config import CONFIG
from utils.AESCipher import AESCipher

cipher = AESCipher(CONFIG.AES_PASSPHRASE)

logger = logging.getLogger(__name__)
logger.setLevel(CONFIG.PG_HTTP_CLIENT_LOGGER_LEVEL)

def make_request(image):
    json_string = json.dumps({"shape": (CONFIG.IMAGE_HEIGHT, CONFIG.IMAGE_WIDTH),
                              "cookie": CONFIG.HTTP_COOKIE})
    data = bytes(json_string, "ascii")
    data += b"\n"  #for easy separation
    data += image.tobytes()

    data = cipher.encrypt(data)

    files = {'data': data}

    try:
        r = requests.post(CONFIG.HTTP_SERVER_URL(), files=files, timeout=10)
    except Exception as e:
        logger.warning('Error communicating with Computational Server, ERR: %s' % str(e))
        return None

    try:
        return r.json()
    except Exception as e:
        logger.warning('Error parsing json, ERR: %s' % str(e))
        return None


if __name__ == '__main__':
    print(make_request(1))