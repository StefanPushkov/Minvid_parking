import unittest

import sqlite3
import time

import os
import sys
# gets path of project directory
def get_base_dir_by_name(name):
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]
sys.path.append(get_base_dir_by_name('carplates_server'))


from pentagon.pg_database import Database
from config import CONFIG

#hack to make local db and keep main db unchanged
CONFIG.DATABASE_PATH = CONFIG.PROJECT_DIR + '/tests/test_res/test_shots.db'

class DatabaseTest(unittest.TestCase):

    def test_db_structure(self):
        db = Database()

        conn = sqlite3.connect(CONFIG.DATABASE_PATH)
        c = conn.cursor()

        query_str = "SELECT * FROM main.sqlite_master WHERE type='table'"
        query = c.execute(query_str)
        table_names = []
        for row in query:
            table_names.append(row[1])

        conn.commit()  # apply changes

        self.assertIn('shots', table_names)


        query_str = 'PRAGMA table_info(' + db.SHOTS_TABLE_NAME + ')'
        query = c.execute(query_str)
        table_fields = []
        for row in query:
            table_fields.append(row[1])

        self.assertListEqual(table_fields, db.SHOTS_FIELDS)

        c.close()
        conn.close()

    #fails at first time if there was no db
    def test_add_shots_concurrent(self):
        db = Database()
        INKAS_AMOUNT = 10
        REPLENISH_AMOUNT = 2

        conn = sqlite3.connect(CONFIG.DATABASE_PATH)
        c = conn.cursor()
        #test that it adds new row
        query_str = 'SELECT count(*) FROM ' + db.SHOTS_TABLE_NAME
        query = c.execute(query_str)
        rows_before = query.fetchall()[0][0]
        c.close()
        conn.close()

        shot_data = {'number': 'AAA111',
                     'frame': '310,285;441,289;441,317;311,313',
                     'plate': '/tmp/..',
                     'image': '/tmp/..',
                     }

        db.add_shot(shot_data)
        db.add_shot(shot_data)
        db.add_shot(shot_data)
        db.add_shot(shot_data)
        time.sleep(1)

        conn = sqlite3.connect(CONFIG.DATABASE_PATH)
        c = conn.cursor()
        query_str = 'SELECT count(*) FROM ' + db.SHOTS_TABLE_NAME
        query = c.execute(query_str)
        rows_after = query.fetchall()[0][0]
        c.close()
        conn.close()

        self.assertTrue(rows_before + 4 == rows_after)

