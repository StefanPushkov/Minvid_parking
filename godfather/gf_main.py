#  This is the daemon for computational service placed on pc with GPU.
#  Interaction is held over http, user data is json encrypted with AES.


import logging
import os
import sys
import threading
import time

import configs.godfather as config

from gf_http_server import GFHandler, ThreadingSimpleServer
from gf_predict import AlprPool
from gf_sqlite import Database

base_dir = config.get_base_dir_by_name('carplates_server')
sys.path.append(base_dir)


class GFMain:
    def __init__(self):
        self.alpr = AlprPool()
        if config.ENABLE_DB:
            self.db = Database()
        self.server = ThreadingSimpleServer((config.HTTP_SERVER_ADDRESS, config.HTTP_SERVER_PORT), GFHandler)
        self.start_server()

    def start_server(self):
        self.server.alpr = self.alpr
        if config.ENABLE_DB:
            self.server.db = self.db
        self.server.alpr.create_workers(config.WORKER_AMOUNT)

        st = threading.Thread(target=self.server.serve_forever)
        st.daemon = True
        st.start()


if __name__ == "__main__":
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    fh = logging.FileHandler(config.LOG_FILE)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=config.LOG_LEVEL, handlers=[ch, fh])
    logging.info('START SERVER')

    GFMain()

    while 1:
        time.sleep(1)
