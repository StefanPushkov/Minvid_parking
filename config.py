import os
import sys
import logging

# gets path of project directory
def get_base_dir_by_name(name):
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]

class Config:
    SOCKET_SERVER_ADRESS = '127.0.0.1'
    SOCKET_SERVER_PORT = 19702
    SOCKET_MAX_THREADS = 4

    #HTTP_SERVER_ADRESS = '127.0.0.1'
    #HTTP_SERVER_ADRESS = '192.168.0.80'
    HTTP_SERVER_ADRESS = '88.119.96.115'
    HTTP_SERVER_PORT = 19840
    HTTP_MAX_THREADS = 4
    HTTP_COOKIE = "KfFdxguMgver6kI"

    AES_PASSPHRASE = "The magic words are squeamish ossifrage"

    def HTTP_SERVER_URL(self):
        return 'http://' + self.HTTP_SERVER_ADRESS + ":" + str(self.HTTP_SERVER_PORT)

    class Entrance:
        name:str = None
        moxa_ip:str = None
        #moxa_dis & cam_ips correspond with each other
        moxa_di_names:list = None
        moxa_dis: list = None
        cam_ips:list = None

        was_pins_active = None #to prevent from multiple shots

        def __init__(self, moxa_ip, moxa_di_names, moxa_dis, cam_ips, name='EMPTY'):
            self.name = name
            self.moxa_ip = moxa_ip
            self.moxa_di_names = moxa_di_names
            self.moxa_dis = moxa_dis
            self.cam_ips = cam_ips

            self.was_pins_active = [False for i in range(len(moxa_dis))]

        def __str__(self):
            return str({'name':self.name, 'moxa_ip':self.moxa_ip,
                        'moxa_di_names':self.moxa_di_names, 'moxa_dis':self.moxa_dis,
                        'cam_ips':self.cam_ips, 'was_pins_active':self.was_pins_active
                        })



    ENTRANCES = [Entrance(name='A1',moxa_ip='192.168.60.50',
                          moxa_di_names=['IN','OUT'],moxa_dis=[0,2],
                          cam_ips=['192.168.60.17','192.168.60.15']),
                 Entrance(name='A2', moxa_ip='192.168.60.51',
                          moxa_di_names=['IN', 'OUT'], moxa_dis=[0, 2],
                          cam_ips=['192.168.60.14', '192.168.60.11']),
                 Entrance(name='K1', moxa_ip='192.168.60.52',
                          moxa_di_names=['OUT_BACK', 'OUT'], moxa_dis=[0, 1],
                          cam_ips=['192.168.60.16', '192.168.60.13']),
                 Entrance(name='K2', moxa_ip='192.168.60.54',
                          moxa_di_names=['IN', 'IN_B'], moxa_dis=[0,-1], #todo no value for IN_B!!!
                          cam_ips=['192.168.60.19', '192.168.60.12']),
                 Entrance(name='K3', moxa_ip='192.168.60.53',
                          moxa_di_names=['IN', 'OUT'], moxa_dis=[0, 2],
                          cam_ips=['192.168.60.10', '192.168.60.18']),
                 Entrance(name='K3_2', moxa_ip='192.168.60.55',
                          moxa_di_names=['OUT_BACK', 'OUT_FRONT'], moxa_dis=[0, 1],
                          cam_ips=['192.168.60.9', '192.168.60.8']),
                ]

    def GEN_MOXA_URL(self, ip:str):
        return  "http://%s/api/slot/0/io/di" % ip

    #def SOCKET_SERVER_URL(self):
    #    return self.SOCKET_SERVER_ADRESS + ":" + str(self.SOCKET_SERVER_PORT)

    #images_root_folder = os.getcwd() + '/output/images'
    images_root_folder = '/tmp/car_shots'
    file_limit_gigabytes = 0.1

    PROJECT_DIR = get_base_dir_by_name('carplates_server')

    stage1_weights = PROJECT_DIR + '/res/gf_res/seg_plates_unet4_model_smart1_0.tf'
    stage2_weights = PROJECT_DIR + '/res/gf_res/seg_chars_unet3_model_smart4.tf'

    DATABASE_NAME = 'shots'
    DATABASE_PATH = PROJECT_DIR + '/res/db/' + DATABASE_NAME + '.db'

    MOXA_LOGGER_LEVEL = logging.INFO
    DB_LOGGER_LEVEL = logging.DEBUG
    CAMERA_LOGGER_LEVEL = logging.DEBUG
    PG_HTTP_CLIENT_LOGGER_LEVEL = logging.DEBUG
    PG_MAIN_LOGGER_LEVEL = logging.DEBUG
    LOG_FILE = PROJECT_DIR + '/main.log'

CONFIG = Config()