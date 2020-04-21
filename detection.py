import time

from colored import commandInfo, debugInfo, detectedInfo, info


class Detector(object):
    """
    Detector class
    """
    def __init__(self):
        self.time = time.time()
        info('Sensor initialed')

    def run(self, signal_queue):
        '''
        `signal_queue`: queue for signals from sensor
        '''
        while True:
            self.time = time.time()
            signal_queue.put(self.time)
            time.sleep(0.1)


if __name__ == "__main__":
    pass
