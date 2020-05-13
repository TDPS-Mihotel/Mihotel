import os
import time

import cv2
import numpy as np

from colored import commandInfo, debugInfo, detectedInfo, info
from controller import GPS, Camera, Compass, DistanceSensor, Robot


class Sensors(object):
    '''
    Sensors interface
    '''
    def __init__(self, robot):
        timestep = int(robot.getBasicTimeStep())

        # enable sensors #######################################################
        self.direction_list = ['front', 'right', 'left', 'path']
        # for each direction, there are three distance sensors
        self.distance_sensors = [[], [], []]
        for i in range(3):
            for j in range(3):
                self.distance_sensors[i].append(robot.getDistanceSensor(
                    self.direction_list[i] + '_' + self.direction_list[j]))
                self.distance_sensors[i][j].enable(timestep)
        # camera frames are received from the main process, so set a default value here
        self.cameras = []
        for i in range(4):
            self.cameras.append(robot.getCamera(self.direction_list[i]))
            self.cameras[i].enable(timestep)
        # compass for moving direction
        self.compass = robot.getCompass('compass')
        self.compass.enable(timestep)
        # GPS for position and speed
        self.gps = robot.getGPS('gps')
        self.gps.enable(timestep)

    def update(self):
        gpsRaw_position = self.gps.getValues()
        gpsRaw_speed = self.gps.getSpeed()
        compassRaw = self.compass.getValues()
        distancesRaw = [self.distance_sensors[i][j].getValue() for i in range(3) for j in range(3)]
        camerasRaw = [item.getImageArray() for item in self.cameras]
        return gpsRaw_position, gpsRaw_speed, compassRaw, distancesRaw, camerasRaw


class Detector(object):
    """
    Detector class
    """
    def __init__(self):
        '''
        `robot`: the Robot() instance
        '''
        # Path_Direction is waiting for Wen Bo
        # Later, various Object_Detection could be added
        self.signals = {
            'Position': [],
            'Direction': [],
            'Speed': [],
            'Front_Distance': [],
            'Right_Distance': [],
            'Left_Distance': [],
            'Color': [],
            'Path_Direction': []
        }

        self.gpsRaw_position = [0, 0, 0]
        self.gpsRaw_speed = [0, 0, 0]
        self.compassRaw = [0, 0, 0]
        self.distancesRaw = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.camerasRaw = [np.zeros((1, 1, 3), np.uint8) for i in range(4)]

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

    def set_queues(self, signal_queue, sensors_queue):
        '''
        `signal_queue`: queue for signals from sensor\n
        `images_queue`: queue for camera frames from main process\n
        '''
        self.signal_queue = signal_queue
        self.sensors_queue = sensors_queue

    def update(self):
        if not self.sensors_queue.empty():
            self.gpsRaw_position, self.gpsRaw_speed, self.compassRaw, self.distancesRaw, self.camerasRaw = self.sensors_queue.get()

    def send_signals(self, signals):
        '''
        `signals`: a dictionary of signals\n
        send out signals through signal_queue
        '''
        self.signal_queue.put(signals)

    def get_image(self, index):
        '''
        capture images from camera to test/camera/
        '''
        image = np.array(self.camerasRaw[index], dtype="uint8")
        r, g, b = cv2.split(image)
        image = cv2.merge([b, g, r])
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, -90, 1.0)
        image = cv2.warpAffine(image, M, (w, h))
        return image

    def capture(self, index):
        '''
        capture images from cameras to test/camera/[index]/
        '''
        capture_path = '../../../test/camera/' + str(index) + '/'
        if not os.path.exists(capture_path):
            os.makedirs(capture_path)
        image = self.get_image(index)
        cv2.imwrite(capture_path + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.png', image)
        info('Captured! 📸')

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
                if key.value == ord('C'):  # capture image when C is pressed
                    self.capture(3)

                # update sensors data
                self.update()
                # update signals
                self.signals['time (min)'] = time.localtime(time.time()).tm_min

                self.signals['Position'] = np.array(self.gpsRaw_position)
                self.signals['Direction'] = np.array(self.compassRaw)
                self.signals['Speed'] = np.array(self.gpsRaw_speed)
                # the minimum distance for each direction where the unit is m.
                self.signals['Front_Distance'] = np.min(self.distancesRaw[0]) / 1000
                self.signals['Right_Distance'] = np.min(self.distancesRaw[1]) / 1000
                self.signals['Left_Distance'] = np.min(self.distancesRaw[2]) / 1000
                self.signals['Color'] = self.get_color(self.get_image(3))

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
