#  This is the daemon for computational service placed on pc with GPU.
#  Interaction is held over http, user data is json encrypted with AES.


import os
import sys
os.chdir(os.getcwd() + '/..')
sys.path.append(os.getcwd())

import threading
import time

from config import CONFIG
from godfather.gf_http_server import GFHandler, ThreadingSimpleServer
from godfather.gf_sekkar import Sekkar

class GFMain:
    def __init__(self):
        self.sekkar = Sekkar()
        self.start_server()

    def start_server(self):
        self.server = ThreadingSimpleServer((CONFIG.HTTP_SERVER_ADRESS, CONFIG.HTTP_SERVER_PORT), GFHandler)
        self.server.predict = self.sekkar.predict # give server a link to prediction method

        st = threading.Thread(target=self.server.serve_forever)
        st.daemon = True
        st.start()



if __name__ == "__main__":
    import logging
    fh = logging.FileHandler(CONFIG.PROJECT_DIR + '/gf_main.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.DEBUG, handlers=[ch, fh])
    logging.critical('START SERVER')

    GFMain()

    while 1:
        time.sleep(1)