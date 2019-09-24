import logging
import os


def get_base_dir_by_name(name):
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]


def http_server_url():
    return 'http://' + HTTP_SERVER_ADDRESS + ":" + str(HTTP_SERVER_PORT)


# [HTTP Settings]
HTTP_SERVER_ADDRESS = '127.0.0.1'
HTTP_SERVER_PORT = 19840
HTTP_COOKIE = "KfFdxguMgver6kI"
AES_PASSPHRASE = "The magic words are squeamish ossifrage"

# [Project Directory]
PROJECT_DIR = get_base_dir_by_name('carplates_server')

# [Multithreading]
WORKER_AMOUNT = 3

# [Database]
ENABLE_DB = True
DB_PATH = '/opt/carplates_server/data/shots.db'
IMAGE_ROOT_FOLDER = '/opt/carplates_server/data/media'

# [Logging]
LOG_FILE = '/var/log/carplates_server/godfather.log'
LOG_LEVEL = logging.DEBUG
