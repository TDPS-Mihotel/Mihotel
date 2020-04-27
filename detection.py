import time

import cv2
import numpy as np

from colored import commandInfo, debugInfo, detectedInfo, info


class Detector(object):
    """
    Detector class
    """

    def __init__(self):
        self.time = time.time()
        info('Sensor initialed')
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

    def run(self, signal_queue, flag_pause):
        '''
        `signal_queue`: queue for signals from sensor\n
        `flag_pause`: the flag to pause this Detector running (actually skip all
            code in this function)\n
        '''
        while True:
            if not flag_pause.value:
                self.time = time.time()
                signal_queue.put(self.time)
                detectedInfo('time:' + str(self.time))
                time.sleep(0.1)

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
