from threading import Thread
import time
import requests
import logging

from config import  CONFIG

logger = logging.getLogger('PGMoxaDriver')
logger.setLevel(CONFIG.MOXA_LOGGER_LEVEL)

class PGMoxaDriver:
    def __init__(self, car_detected_callback):
        self.car_detected_callback = car_detected_callback
        self._start()

    ##### Start lifecycle functions #####
    def _start(self):
        self.thread = Thread(target=self._loop)
        self.isActive = True
        self.thread.start()

    def stop(self):
        self.isActive = False

    def _loop(self):
        while(self.isActive):
            logger.debug('START NEW REQUEST CYCLE')
            for entrance in CONFIG.ENTRANCES:
                moxa_url = CONFIG.GEN_MOXA_URL(entrance.moxa_ip)
                try:
                    r = requests.get(moxa_url,
                                     timeout=1,
                                     headers={'Content-Type': "application/json",
                                              "Accept": 'vdn.dac.v1'})
                except Exception as e:
                    logger.warning('Error requesting moxa with url %s, ERR: %s' % (moxa_url,str(e)))
                    continue

                logger.debug('Got response: ' + str(r.content))

                di = r.json()['io']['di']

                for di_pin in di:
                    for i in range(len(entrance.moxa_dis)):
                        if di_pin['diIndex'] != entrance.moxa_dis[i]:
                            continue
                        if di_pin['diStatus'] == 0:
                            if entrance.was_pins_active[i]:
                                logger.debug('Pin deactivated: %s in ENTRANCE: %s' %
                                             (str(di_pin['diIndex']), str(entrance))
                                             )
                            entrance.was_pins_active[i] = False
                        if di_pin['diStatus'] == 1:
                            if entrance.was_pins_active[i]:
                                continue
                            logger.debug('Pin activated: %s in ENTRANCE: %s' % (str(di_pin), str(entrance)))
                            entrance.was_pins_active[i] = True

                            self.car_detected_callback(entrance.cam_ips[i])


            time.sleep(0.5)

    ##### End lifecycle functions #####
