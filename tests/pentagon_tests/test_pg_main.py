import unittest

import os
import sys
# gets path of project directory
def get_base_dir_by_name(name):
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]
sys.path.append(get_base_dir_by_name('carplates_server'))

from config import CONFIG

CONFIG.ENTRANCES = [CONFIG.Entrance(name='TEST',moxa_ip='127.0.0.1:%s' % str(PORT),
                          moxa_di_names=['IN','OUT'],moxa_dis=[0,1],
                          cam_ips=['192.168.60.17','192.168.60.15']),
                    ]
CONFIG.DATABASE_PATH = CONFIG.PROJECT_DIR + '/tests/test_res/test_shots.db'

from pentagon.pg_main import PGMain
from api.a_socket_client import make_shot

class PGMainTest(unittest.TestCase):
    @unittest.skip('Run only on production server where it is a camera. Also godfather should work')
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