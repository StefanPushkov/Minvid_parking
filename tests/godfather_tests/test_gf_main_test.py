import unittest


import os
import cv2
import json
import requests

from godfather.gf_main import GFMain
from config import CONFIG

class GFMainTest(unittest.TestCase):
    @unittest.skip('Image recognition is computationally costly')
    def test_answer(self):
        GFMain()

        image = cv2.imread(os.getcwd() + '/test_res/152386286686123_full.png', 0)

        files = {'shape': str(json.dumps(image.shape)), 'image': image.tobytes()}

        r = requests.post(CONFIG.HTTP_SERVER_URL(), headers={'Content-Type': 'image/gif'}, files=files)
        print(r.json())

        self.assertEqual(r.json(), {'status': 1, 'number': 'AEERG964', 'frame': '515,215;627,219;626,241;513,238', 'confidence': 100})


if __name__ == "__main__":
    unittest.main()