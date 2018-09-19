First of all:

1. edit config.py


To install computational service (godfather):

1. cp godfather/carplates_server_gf.service /etc/systemd/system/
2. systemctl enable carplates_server_gf.service
3. systemctl start carplates_server_gf.service
4. systemctl status carplates_server_gf.service


To install image grabbing service (pentagon):

1. cp pentagon/carplates_server_gf.service /etc/systemd/system/
2. systemctl enable carplates_server_pg.service
3. systemctl start carplates_server_pg.service
4. systemctl status carplates_server_pg.service


To call image grabbing service:

from api.a_socket_client import make_shot
camera_ip = "192.168.60.9"
make_shot(camera_ip)