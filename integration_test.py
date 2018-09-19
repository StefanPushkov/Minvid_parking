from godfather.gf_main import GFMain
from pentagon.pg_main import PGMain
from api.a_socket_client import make_shot

#GFMain()

import time
import threading


#pg = PGMain()

start_time = time.time()

def threaded_f():
    print(make_shot('/media/data/server_img/analyze/152386286686123_full.png'))

threads = []
for i in range(1):
    t = threading.Thread(target=threaded_f)
    t.start()
    threads.append(t)

for i in range(1):
    threads[i].join()


print(time.time() - start_time)

#pg.stop()
