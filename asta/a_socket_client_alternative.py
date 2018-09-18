import socket
import json

from config import Config
config = Config()

'''
shot_data = {
    'status': 1, # OK, other error statuses: /var/www/parking/project/apps/cameras/models.py from line 89 STATUS_OK = 1
    'number': 'AAA111',
    'frame': '310,285;441,289;441,317;311,313' # plateno coordinates in photo
    'confidence': 90, # percent
    'plate': '/tmp/..', # path to cropped plateno fame, not used now
    'image': '/tmp/..', # path to photo
}
'''

def make_shot(shot_path):
    json_obj = None
    # try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.settimeout(8.0)
    client.connect((config.SOCKET_SERVER_ADRESS, config.SOCKET_SERVER_PORT))

    client.send(str.encode(shot_path))
    json_bytes = client.recv(4096)

    json_string = json_bytes.decode('utf8')
    json_obj = json.loads(json_string)

    client.shutdown(socket.SHUT_RDWR)
    client.close()

    '''
        except Exception as msg:
        json_obj = {
            'status': -3,
            'error': msg
        }
    '''
    return json_obj



if __name__ == '__main__':
    print(make_shot('/media/data/server_img/analyze/152386286686123_full.png'))