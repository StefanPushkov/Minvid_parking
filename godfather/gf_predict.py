import logging
import queue
import threading

from openalpr import Alpr


def _create_worker(task_queue, result_queue):
    AlprPredict(task_queue, result_queue)


class AlprPool:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()

        self.task_counter = 0

    def create_workers(self, amount):
        for _ in range(0, amount):
            thread = threading.Thread(target=_create_worker, args=(self.task_queue, self.result_queue))
            thread.start()

    def predict(self, image: bytes):
        self.task_queue.put(image)
        self.task_counter += 1

    def block_until_done(self):
        while self.result_queue.qsize() < self.task_counter:
            continue
        return

    def get_results(self):
        self.task_counter = 0
        while True:
            try:
                yield self.result_queue.get_nowait()
            except queue.Empty:
                break


class AlprPredict:
    def __init__(self, task_queue, result_queue):
        self.alpr = Alpr('eu', '/usr/share/openalpr/config/openalpr.defaults.conf',
                         '/usr/share/openalpr/runtime_data')
        self.alpr.set_top_n(1)
        self.alpr.set_default_region('lt')

        self.task_queue = task_queue
        self.result_queue = result_queue

        self.run()

    def run(self):
        while True:
            self.predict()

    def predict(self):
        image = self.task_queue.get()

        result = None
        try:
            recog_results = self.alpr.recognize_array(image)['results']

            if len(recog_results) != 0:
                result = recog_results[0]['plate']
        except Exception as e:
            logging.error(e)
            result['status'] = 0

        self.result_queue.put(result)
