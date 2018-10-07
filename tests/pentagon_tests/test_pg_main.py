import unittest

import os
import sys

print(os.getcwd())
sys.path.append(os.getcwd())

PORT = 9999

from config import CONFIG

CONFIG.ENTRANCES = [CONFIG.Entrance(name='TEST',moxa_ip='127.0.0.1:%s' % str(PORT),
                          moxa_di_names=['IN','OUT'],moxa_dis=[0,1],
                          cam_ips=['192.168.60.17','192.168.60.15']),
                    ]
CONFIG.DATABASE_PATH = CONFIG.PROJECT_DIR + '/tests/test_res/test_shots.db'

from pentagon.pg_main import PGMain
from api.a_socket_client import make_shot

import json
import time
from threading import Thread

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

    #@unittest.skip('Run only on production server where it is a camera. Also godfather should work')
    #tests how moxa drivr works
    def test_shooting_on_moxa(self):
        from http.server import BaseHTTPRequestHandler, HTTPServer
        class Handler(BaseHTTPRequestHandler):
            is_moxa_di_0_active = False
            is_moxa_di_1_active = False

            def __init__(self):
                super().__init__()
                self.server.hook(self)

            def do_GET(self):
                if self.path != '/api/slot/0/io/di':
                    print('wrong path!')
                    self.send_response(404)
                    self.wfile.write(b'')
                    return

                self.send_response(200)
                self.end_headers()

                moxa_state = {'slot': 0,
                              'io': {'di': [{'diIndex': 0, 'diMode': 0, 'diStatus': self.is_moxa_di_0_active},
                               {'diIndex': 1, 'diMode': 0, 'diStatus': self.is_moxa_di_1_active},
                               {'diIndex': 2, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 3, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 4, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 5, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 6, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 7, 'diMode': 0, 'diStatus': 0}]}}

                string = json.dumps(moxa_state)
                self.wfile.write(bytes(string, 'utf8'))
                return

        handler_instance = None
        def set_handler_instance(hi):
            global handler_instance
            handler_instance = hi
        server = HTTPServer(('127.0.0.1', PORT), Handler)
        server.hook = lambda x: set_handler_instance(x)
        st = Thread(target=server.serve_forever)
        st.daemon = True
        st.start()

        pgm = PGMain()
        pgm.db.c.execute('DELETE FROM %s' % pgm.db.SHOTS_TABLE_NAME)

        if handler_instance is None:
            print("error, cannot get handler instance")
            return

        time.sleep(2)
        print('Activating coil 1')
        handler_instance.is_moxa_di_0_active = True
        time.sleep(5)
        print('Deactivating coil 1')
        handler_instance.is_moxa_di_0_active = False

        print('Activating coil 2')
        handler_instance.is_moxa_di_1_active = True
        time.sleep(5)
        print('Deactivating coil 2')
        handler_instance.is_moxa_di_1_active = False

        query_str = 'SELECT count(*) FROM ' + pgm.db.SHOTS_TABLE_NAME
        query = pgm.db.c.execute(query_str)
        num_rows_added = query.fetchall()[0][0]
        print('Totally added %d rows' % num_rows_added)

        self.assertEqual(num_rows_added, 2)


if __name__ == "__main__":
    unittest.main()