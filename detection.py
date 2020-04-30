import time

import cv2
import numpy as np

from colored import commandInfo, debugInfo, detectedInfo, info


class Detector(object):
    """
    Detector class
    """

    def __init__(self):
        self.signals = {}
        self.color_list = [
            ('black', np.array([0, 0, 0]), np.array([180, 255, 46])),
            ('white', np.array([0, 0, 221]), np.array([180, 30, 255])),
            ('red', np.array([156, 43, 46]), np.array([180, 255, 255])),
            ('red', np.array([0, 43, 46]), np.array([10, 255, 255])),
            ('orange', np.array([11, 43, 46]), np.array([25, 255, 255])),
            ('yellow', np.array([26, 43, 46]), np.array([34, 255, 255])),
            ('green', np.array([35, 43, 46]), np.array([77, 255, 255])),
            ('cyan', np.array([78, 43, 46]), np.array([99, 255, 255])),
            ('blue', np.array([100, 43, 46]), np.array([124, 255, 255])),
            ('purple', np.array([125, 43, 46]), np.array([155, 255, 255]))
        ]
        info('Sensor initialed')

    def set_queues(self, signal_queue):
        '''
        `signal_queue`: queue for signals from sensor\n
        '''
        self.signal_queue = signal_queue

    def send_signals(self, signals):
        '''
        `signals`: a dictionary of signals\n
        send out signals through signal_queue
        '''
        self.signal_queue.put(signals)

    def capture(self):
        '''
        capture images from camera to test/camera/
        '''
        # TODO: for Haoran
        pass

    def get_color(self, frame):
        """
        Get the principal color of the image\n
        `param frame`: Input image\n
        `return color`: Principal color of the image
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # cvt rgb to hsv
        maxsum = -100
        color = None
        for item in self.color_list:
            mask = cv2.inRange(hsv, item[1], item[2])  # set regions of other colors to black
            binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]  # threshold images into binary type
            binary = cv2.dilate(binary, None, iterations=2)
            contours, hierarchy = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            sum = 0
            for c in contours:
                sum += cv2.contourArea(c)
            if sum > maxsum:
                maxsum = sum
                color = item[0]
        return color

    def run(self, flag_pause, key):
        '''
        `flag_pause`: the flag to pause this Detector running (actually skips code in this function)\n
        run the detection
        '''
        while True:
            time.sleep(0.1)  # set detection period to 0.1s
            # skip all code inside if paused by webots
            if not flag_pause.value:
                # vision/sensor group's code goes under this ###################
                # keyboard events
                # TODO: save image from camera for Haoran
                if key.value == ord('S'):  # capture image when press S
                    self.capture()

                # update signals
                self.signals['time (min)'] = time.localtime(time.time()).tm_min
                self.signals['time (sec)'] = time.localtime(time.time()).tm_sec

                # send all signals to decider
                self.send_signals(self.signals)
                debugInfo('\n\t'.join([str(item) + ': ' + str(self.signals[item]) for item in self.signals]))


if __name__ == "__main__":
    detector = Detector()
    img1 = './test/imgs/lena.jpg'
    img2 = './test/imgs/mihotel.jpg'
    img3 = './test/imgs/bird.jpg'
    frame1 = cv2.imread(img1)
    frame2 = cv2.imread(img2)
    frame3 = cv2.imread(img3)
    print(detector.get_color(frame1), detector.get_color(frame2), detector.get_color(frame3))
    # Expected output: red white cyan
