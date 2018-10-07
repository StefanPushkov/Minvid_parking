import os
import sys
# gets path of project directory
def get_base_dir_by_name(name):
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]
sys.path.append(get_base_dir_by_name('carplates_server'))

PORT = 9998

from config import CONFIG

CONFIG.ENTRANCES = [CONFIG.Entrance(name='TEST',moxa_ip='127.0.0.1:%s' % str(PORT),
                          moxa_di_names=['IN','OUT'],moxa_dis=[0,1],
                          cam_ips=['192.168.60.17','192.168.60.15']),
                    ]
CONFIG.DATABASE_PATH = CONFIG.PROJECT_DIR + '/tests/test_res/test_shots.db'

from pentagon.pg_main import PGMain

import json
import time
from threading import Thread

class PGMainTest():
    #tests how moxa drivr works
    def test_shooting_on_moxa(self):
        from http.server import BaseHTTPRequestHandler, HTTPServer
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != '/api/slot/0/io/di':
                    print('wrong path: ' + self.path)
                    self.send_response(404)
                    self.wfile.write(b'')
                    return

                self.send_response(200)
                self.end_headers()

                is_moxa_di_0_active, is_moxa_di_1_active = self.server.hook()

                moxa_state = {'slot': 0,
                              'io': {'di': [{'diIndex': 0, 'diMode': 0, 'diStatus': is_moxa_di_0_active},
                               {'diIndex': 1, 'diMode': 0, 'diStatus': is_moxa_di_1_active},
                               {'diIndex': 2, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 3, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 4, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 5, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 6, 'diMode': 0, 'diStatus': 0},
                               {'diIndex': 7, 'diMode': 0, 'diStatus': 0}]}}

                string = json.dumps(moxa_state)
                self.wfile.write(bytes(string, 'utf8'))
                return

        is_moxa_di_0_active = 0
        is_moxa_di_1_active = 0

        def get_moxa_activity():
            return is_moxa_di_0_active, is_moxa_di_1_active

        server = HTTPServer(('127.0.0.1', PORT), Handler)
        server.hook = lambda : get_moxa_activity()
        st = Thread(target=server.serve_forever)
        st.daemon = True
        st.start()
        time.sleep(2)

        pgm = PGMain()
        pgm.db.c.execute('DELETE FROM %s' % pgm.db.SHOTS_TABLE_NAME)

        time.sleep(2)
        print('Activating coil 1')
        is_moxa_di_0_active = 1
        time.sleep(2)
        print('Deactivating coil 1')
        is_moxa_di_0_active = 0

        print('Activating coil 2')
        is_moxa_di_1_active = 1
        time.sleep(2)
        print('Deactivating coil 2')
        is_moxa_di_1_active = 0

        query_str = 'SELECT count(*) FROM ' + pgm.db.SHOTS_TABLE_NAME
        query = pgm.db.c.execute(query_str)
        pgm.db.conn.commit()
        num_rows_added = query.fetchall()[0][0]
        print('Totally added %d rows' % num_rows_added)

        if num_rows_added != 2:
            print('ERROR, NUMBER OF ROWS IN DB DO NOT MATCH!')


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    pgmt = PGMainTest()
    pgmt.test_shooting_on_moxa()