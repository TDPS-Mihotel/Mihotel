import time

from colored import debugInfo, detectedInfo, info, movementInfo


class Sensor(object):
    """
    sensor class
    """

    def __init__(self):
        self.time = time.time()
        info('Sensor initialed')

    def run(self, sense_queue):
        while True:
            self.time = time.time()
            sense_queue.put(self.time)
            time.sleep(0.1)
