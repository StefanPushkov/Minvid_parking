import os

class Config:
    SOCKET_SERVER_ADRESS = '127.0.0.1'
    SOCKET_SERVER_PORT = 19702
    SOCKET_MAX_THREADS = 4

    HTTP_SERVER_ADRESS = '127.0.0.1'
    #HTTP_SERVER_ADRESS = '192.168.0.80'
    HTTP_SERVER_PORT = 19840
    HTTP_MAX_THREADS = 4
    HTTP_COOKIE = "KfFdxguMgver6kI"

    AES_PASSPHRASE = "The magic words are squeamish ossifrage"

    def HTTP_SERVER_URL(self):
        return 'http://' + self.HTTP_SERVER_ADRESS + ":" + str(self.HTTP_SERVER_PORT)

    #def SOCKET_SERVER_URL(self):
    #    return self.SOCKET_SERVER_ADRESS + ":" + str(self.SOCKET_SERVER_PORT)

    images_root_folder = os.getcwd() + '/output/images'
    file_limit_gigabytes = 0.1

    project_dir = '/media/ydisk/yandex-disk/a_programming/pyProjects/SMART_KPP/carplates_server'
    #project_dir = os.getcwd()
    stage1_weights = project_dir + '/res/gf_res/seg_plates_unet4_model_smart1_0.tf'
    stage2_weights = project_dir + '/res/gf_res/seg_chars_unet3_model_smart4.tf'

CONFIG = Config()