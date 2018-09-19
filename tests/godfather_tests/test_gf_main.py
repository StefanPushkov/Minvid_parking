import unittest


import os
import cv2
import sys
print(os.getcwd())
sys.path.append(os.getcwd())

from godfather.gf_main import GFMain
from pentagon.pg_http_client import make_request
from config import CONFIG

class GFMainTest(unittest.TestCase):
    @unittest.skip('Image recognition is computationally costly')
    def test_answer(self):
        GFMain()

        image = cv2.imread(CONFIG.project_dir + '/tests/test_res/152386286686123_full.png', 0)

        json_object = make_request(image)

        print(json_object)

        self.assertEqual(json_object, {'status': 1, 'number': 'AEERG964', 'frame': '515,215;627,219;626,241;513,238', 'confidence': 100})

    #@unittest.skip('Only if godfather works')
    def test_answer(self):
        image = cv2.imread(CONFIG.project_dir + '/tests/test_res/152386286686123_full.png', 0)

        json_object = make_request(image)

        print(json_object)

        self.assertEqual(json_object, {'status': 1, 'number': 'AEERG964', 'frame': '515,215;627,219;626,241;513,238',
                                       'confidence': 100})


if __name__ == "__main__":
    unittest.main()