import os
import logging


# [Utility Functions and Classes]
def get_base_dir_by_name(name):
    """
    Gets path of project directory
    :param name: Project name
    :return: Project directory path
    """
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]


def gen_moxa_url(ip: str):
    return "http://%s/api/slot/0/io/di" % ip


def http_server_url():
    return 'http://' + HTTP_SERVER_ADDRESS + ":" + str(HTTP_SERVER_PORT)


class Entrance:
    name = None
    moxa_ip = None
    # moxa_dis & cam_ips correspond with each other
    moxa_di_names = None
    moxa_dis = None
    cam_ips = None

    was_pins_active = None

    def __init__(self, moxa_ip, moxa_di_names, moxa_dis, cam_ips, name='EMPTY'):
        self.name = name
        self.moxa_ip = moxa_ip
        self.moxa_di_names = moxa_di_names
        self.moxa_dis = moxa_dis
        self.cam_ips = cam_ips

        self.was_pins_active = [False] * len(moxa_dis)

    def __str__(self):
        return str({'name': self.name, 'moxa_ip': self.moxa_ip,
                    'moxa_di_names': self.moxa_di_names, 'moxa_dis': self.moxa_dis,
                    'cam_ips': self.cam_ips, 'was_pins_active': self.was_pins_active
                    })


# [HTTP Settings]
HTTP_SERVER_ADDRESS = '127.0.0.1'
HTTP_SERVER_PORT = 19840
HTTP_COOKIE = "KfFdxguMgver6kI"
AES_PASSPHRASE = "The magic words are squeamish ossifrage"

# [Socket Settings]
SOCKET_SERVER_ADDRESS = '127.0.0.1'
SOCKET_SERVER_PORT = 19702
SOCKET_MAX_THREADS = 4

# [Utility Paths]
PROJECT_DIR = get_base_dir_by_name('carplates_server')

# [Image Properties]
IMAGE_HEIGHT = 1136
IMAGE_WIDTH = 1920

# [Photo Series Properties]
PHOTO_SERIES_SIZE = 9
SHOT_INTERVAL = 50  # ms

# [Logging]
LOG_LEVEL = logging.INFO
LOG_FILE = '/var/log/carplates_server/pentagon.log'

# [MOXA Entrances]
ENTRANCES = [Entrance(name='A1', moxa_ip='192.168.60.50',
                      moxa_di_names=['IN', 'OUT'], moxa_dis=[0, 2],
                      cam_ips=['192.168.60.17', '192.168.60.15']),
             Entrance(name='A2', moxa_ip='192.168.60.51',
                      moxa_di_names=['IN', 'OUT'], moxa_dis=[0, 2],
                      cam_ips=['192.168.60.14', '192.168.60.11']),
             Entrance(name='K1', moxa_ip='192.168.60.52',
                      moxa_di_names=['OUT_BACK', 'OUT'], moxa_dis=[0, 1],
                      cam_ips=['192.168.60.16', '192.168.60.13']),
             Entrance(name='K2', moxa_ip='192.168.60.54',
                      moxa_di_names=['IN', 'IN_B'], moxa_dis=[0, -1],
                      cam_ips=['192.168.60.19', '192.168.60.12']),
             Entrance(name='K3', moxa_ip='192.168.60.53',
                      moxa_di_names=['IN', 'OUT'], moxa_dis=[0, 2],
                      cam_ips=['192.168.60.10', '192.168.60.18']),
             Entrance(name='K3_2', moxa_ip='192.168.60.55',
                      moxa_di_names=['OUT_BACK', 'OUT_FRONT'], moxa_dis=[0, 1],
                      cam_ips=['192.168.60.9', '192.168.60.8']),
             ]
