import sqlite3
import json
from threading import Thread
from queue import Queue
import logging

from config import CONFIG

logger = logging.getLogger(__name__)
logger.setLevel(CONFIG.DB_LOGGER_LEVEL)

class Database:

    SHOTS_TABLE_NAME = 'shots'
    '''
    CARS_FIELDS = ['id', 'shot_id', 'plateno', 'plate_frame',
                       'plate_image', 'full_image', 'confidence',
                       'status', 'created_at', 'camera_id']
    '''
    SHOTS_FIELDS = ['plateno', 'plate_frame', 'plate_image', 'full_image']

    is_active = False

    def __init__(self):
        conn = sqlite3.connect(CONFIG.DATABASE_PATH)
        c = conn.cursor()

        statementcars = 'CREATE TABLE IF NOT EXISTS ' + self.SHOTS_TABLE_NAME + ' ('
        for i in range(len(self.SHOTS_FIELDS)):
            statementcars += self.SHOTS_FIELDS[i] + ' text, '
        statementcars = statementcars[:-2] + ')'
        c.execute(statementcars)
        self._start()

    def _start(self):
        self.is_active = True
        self.queue = Queue()
        t = Thread(target=self._loop)
        t.setDaemon(True)
        t.start()

    def stop(self):
        #self.is_active = False #stop on the next iteration (if lots in the queue)
        self.queue.put(None) #stop if nothing in the queue


    def _loop(self):
        while self.is_active:
            json_obj = self.queue.get()

            if json_obj is None:
                break

            if 'number' not in json_obj \
                    or 'frame' not in json_obj \
                    or 'plate' not in json_obj \
                    or 'image' not in json_obj:
                logger.warning('Cannot add shot to db, wrong json: ' + json.dumps(json_obj))
                self.queue.task_done()
                continue

            conn = sqlite3.connect(CONFIG.DATABASE_PATH)
            c = conn.cursor()

            query = 'INSERT INTO ' + self.SHOTS_TABLE_NAME + ' VALUES (?,?,?,?)'
            values = [json_obj['number'], json_obj['frame'], json_obj['plate'], json_obj['image']]
            values = list(map(str, values))  # conversion of int (values[0]) to str is ok here
            c.executemany(query, [values])  # actually executes only once

            conn.commit()  # apply changes
            c.close()
            conn.close()

            logger.info('Added to db: ' + json.dumps(json_obj))

            self.queue.task_done()


    def add_shot(self, json_obj):
        self.queue.put(json_obj)