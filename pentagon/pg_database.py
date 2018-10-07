import sqlite3
from datetime import datetime

from config import CONFIG

class Database:

    SHOTS_TABLE_NAME = 'shots'
    '''
    CARS_FIELDS = ['id', 'shot_id', 'plateno', 'plate_frame',
                       'plate_image', 'full_image', 'confidence',
                       'status', 'created_at', 'camera_id']
    '''
    SHOTS_FIELDS = ['plateno', 'plate_frame', 'plate_image', 'full_image']

    def __init__(self):
        self.conn = sqlite3.connect(CONFIG.DATABASE_PATH)
        self.c = self.conn.cursor()

        statementcars = 'CREATE TABLE IF NOT EXISTS ' + self.SHOTS_TABLE_NAME + ' ('
        for i in range(len(self.SHOTS_FIELDS)):
            statementcars += self.SHOTS_FIELDS[i] + ' text, '
        statementcars = statementcars[:-2] + ')'
        self.c.execute(statementcars)

    def close(self):
        self.c.close()
        self.conn.close()


    def add_shot(self, json_obj):

        query = 'INSERT INTO ' + self.SHOTS_TABLE_NAME + ' VALUES (?,?,?,?)'
        values = [json_obj['number'], json_obj['frame'], json_obj['plate'], json_obj['image']]
        values = list(map(str, values)) #conversion of int (values[0]) to str is ok here
        self.c.executemany(query, [values])  # actually executes only once
        self.conn.commit() #apply changes