import unittest

import os
import sys

print(os.getcwd())
sys.path.append(os.getcwd())

from pentagon.pg_main import PGMain
from api.a_socket_client import make_shot

class PGMainTest(unittest.TestCase):
    @unittest.skip('Run only on production server where it is a camera. Also godrather should work')
    def test_make_shot(self):
        pgm = PGMain()

        json_answer = make_shot('192.168.60.9')

        pgm.stop()

        print("json_answer", json_answer)

        self.assertTrue(json_answer['status'] == 1)

    @unittest.skip('Run on production server. Both godfather and pentagon services should work')
    def test_make_shot2(self):
        json_answer = make_shot('192.168.60.9')

        print("json_answer", json_answer)

        self.assertTrue(json_answer['status'] == 1)


if __name__ == "__main__":
    unittest.main()