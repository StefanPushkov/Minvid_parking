import os
import random
import sqlite3
import string
from threading import Thread
from queue import Queue
import logging

import configs.godfather as config

logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)


def _get_image_path(plate):
    image_name = plate + '_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) + '.jpg'
    image_path = config.IMAGE_ROOT_FOLDER + '/' + image_name
    return image_name, image_path


class Database:

    SHOTS_TABLE_NAME = 'shots'
    '''
    CARS_FIELDS = ['id', 'shot_id', 'plateno',
                   'full_image', 'confidence',
                   'status', 'created_at', 'camera_id']
    '''
    SHOTS_FIELDS = ['plateno', 'full_image']

    is_active = False

    def __init__(self):
        os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
        conn = sqlite3.connect(config.DB_PATH)
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
        self.queue.put(None)

    def _loop(self):
        while self.is_active:
            number, image = self.queue.get()

            if not number:
                break

            image_name, image_path = _get_image_path(number)

            json_obj = {
                'number': number,
                'image': image_name
            }

            conn = sqlite3.connect(config.DB_PATH)
            c = conn.cursor()

            query = 'INSERT INTO ' + self.SHOTS_TABLE_NAME + ' VALUES (?,?)'
            values = [json_obj['number'], json_obj['image']]
            values = list(map(str, values))  # conversion of int (values[0]) to str is ok here
            c.executemany(query, [values])  # actually executes only once

            conn.commit()  # apply changes
            c.close()
            conn.close()

            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, 'wb') as outfile:
                outfile.write(image)

            logger.info('Added to db: ' + json_obj['number'])

            self.queue.task_done()

    def add_shot(self, number, image):
        self.queue.put((number, image))
