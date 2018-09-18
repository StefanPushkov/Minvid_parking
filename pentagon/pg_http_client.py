# Client that makes request to a production server


import requests
import cv2
import json

from config import CONFIG
from utils.AESCipher import AESCipher

cipher = AESCipher(CONFIG.AES_PASSPHRASE)

def make_request(image):
    image = cv2.imread('/media/data/server_img/analyze/152386286686123_full.png', 0)

    json_string = json.dumps({"shape": (480, 752), "cookie": CONFIG.HTTP_COOKIE})
    data = bytes(json_string, "ascii")
    data += b"\n"  #for easy separation
    data += image.tobytes()

    data = cipher.encrypt(data)

    files = {'data': data}

    r = requests.post(CONFIG.HTTP_SERVER_URL(), files=files)

    #print(r.status_code)
    #print(r.headers)
    #print(r.content)

    return r.json()

if __name__ == '__main__':
    print(make_request(1))