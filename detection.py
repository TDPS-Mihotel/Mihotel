import os
import queue
import time

import cv2
import numpy as np

from colored import commandInfo, debugInfo, detectedInfo, info


class Sensors(object):
    '''
    Sensors interface
    '''

    def __init__(self, robot):
        '''
        `robot`: the Robot() instance from main process
        '''
        # TODO: refactor to use dict after the solution is decided
        from controller import GPS, Camera, Compass, DistanceSensor
        timestep = int(robot.getBasicTimeStep())

        # enable sensors #######################################################
        self.direction_list = ['front', 'right', 'left', 'path']
        # for each direction, there are three distance sensors
        self.distance_sensors = []
        for i in range(3):
            self.distance_sensors.append(robot.getDistanceSensor(self.direction_list[i] + '_ds'))
            self.distance_sensors[i].enable(timestep)
        # camera frames are received from the main process, so set a default value here
        self.cameras = []
        for i in range(4):
            self.cameras.append(robot.getCamera(self.direction_list[i] + '_cam'))
            self.cameras[i].enable(timestep)
        # compass for moving direction
        self.compass = robot.getCompass('compass')
        self.compass.enable(timestep)
        # GPS for position and speed
        self.gps = robot.getGPS('gps')
        self.gps.enable(timestep)

    def update(self):
        '''
        get and return `gpsRaw_position`, `gpsRaw_speed`, `compassRaw`, `distancesRaw`, `camerasRaw`
        '''
        gpsRaw_position = self.gps.getValues()
        gpsRaw_speed = self.gps.getSpeed()
        compassRaw = self.compass.getValues()
        distancesRaw = [self.distance_sensors[i].getValue() for i in range(3)]
        camerasRaw = [item.getImageArray() for item in self.cameras]
        return (
            gpsRaw_position,
            gpsRaw_speed,
            compassRaw,
            distancesRaw,
            camerasRaw
        )


class Detector(object):
    """
    Detector class
    """

    def __init__(self):
        # TODO: Path_Direction is waiting for Wen Bo
        # Later, various Object_Detection could be added
        self.signals = {
            'Position': [],
            'Direction_x': [],
            'Direction_-z': [],
            'Speed': [],
            'Distance': [],
            'Color': [],
            'Path_Direction': []
        }

        self.gpsRaw_position = [0, 0, 0]
        self.gpsRaw_speed = [0, 0, 0]
        self.compassRaw = [1, 0, 0]
        self.distancesRaw = [[0, 0, 0]]
        self.camerasRaw = [np.zeros((128, 128, 3), np.uint8) for i in range(4)]

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

        self.car_location = np.array([120, 64])
        self.car_leftedge = 42
        self.car_rightedge = 87

    def set_queues(self, signal_queue, sensors_queue):
        '''
        `signal_queue`: queue for signals from sensor\n
        `sensors_queue`: queue for sensors raw data from main process\n
        '''
        self.signal_queue = signal_queue
        self.sensors_queue = sensors_queue

    def update(self):
        '''
        update `gpsRaw_position`, `gpsRaw_speed`, `compassRaw`, `distancesRaw`, `camerasRaw` received from main process
        '''
        while True:
            try:
                (
                    self.gpsRaw_position,
                    self.gpsRaw_speed,
                    self.compassRaw,
                    self.distancesRaw,
                    self.camerasRaw
                ) = self.sensors_queue.get(block=True, timeout=0.05)
            except queue.Empty:
                break

    def send_signals(self, signals):
        '''
        `signals`: a dictionary of signals\n
        send out signals through signal_queue
        '''
        self.signal_queue.put(signals)

    def get_image(self, index):
        '''
        convert format and direction of image from webots camera\n
        `index`: index of the camera
        '''
        image = np.array(self.camerasRaw[index], dtype="uint8")
        r, g, b = cv2.split(image)
        image = cv2.merge([b, g, r])
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, -90, 1.0)
        image = cv2.warpAffine(image, M, (w, h))
        image = image[5:133, 5:133]
        image = cv2.flip(image, 1)
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
            sum = np.sum(binary)
            if sum > maxsum:
                maxsum = sum
                color = item[0]
        return color

    def rec2angle(self, x):
        '''
        Convert the direction which is originally in the Cartesian system to the angle.
        return: the direction that the head deviate from the x-axis, whose range is [-180 180]
        '''
        x = np.array(x)
        angle = 180 * np.arctan(x[1] / x[0]) / np.pi
        if x[0] < 0:
            if x[1] > 0:
                angle = angle + 180
            else:
                angle = angle - 180
        return angle

    def path_detection(self):
        '''
        This algorithm gives the angle of the direction of the path
        Written by Wen Bo
        '''
        image = self.get_image(3)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        new_size = 16
        threshold_gray = 70

        location = np.argwhere((image_gray[0:new_size, 0:128]) <= threshold_gray)
        (f_y, f_x) = np.mean(a=location, axis=0)

        degree = self.rec2angle([102 - f_y, f_x - 64])
        return degree

    def run(self, flag_pause, key):
        '''
        run the detection
        `flag_pause`: the flag to pause this Detector running (actually skips code in this function)\n
        `key`: ascii number of pressed key on keyboard, is -1 when no key pressed
        '''
        while True:
            # time.sleep(0.1)  # set detection period to 0.1s
            # skip all code inside if paused by webots
            if not flag_pause.value:
                # keyboard events
                if key.value == ord('C'):  # capture image when C is pressed
                    self.capture(3)

                # update sensors data
                self.update()
                # update signals
                self.signals['time'] = time.strftime("%H:%M:%S", time.localtime())

                self.signals['Position'] = np.array(self.gpsRaw_position)
                self.signals['Direction_x'] = self.rec2angle(self.compassRaw[:2])
                self.signals['Direction_-z'] = self.rec2angle([-self.compassRaw[1], self.compassRaw[0]])
                self.signals['Speed'] = np.array(self.gpsRaw_speed)
                # the minimum distance for each direction where the unit is m.
                self.signals['Distance'] = np.min(self.distancesRaw) / 1000
                self.signals['Color'] = self.get_color(self.get_image(3))
                self.signals['Path_Direction'] = self.path_detection()

                self.path_detection()
                # send all signals to decider
                self.send_signals(self.signals)
                debugInfo('\n        '.join([str(item) + ': ' + str(self.signals[item]) for item in self.signals]))


if __name__ == "__main__":
    detector = Detector()
    img1 = './test/img/lena.jpg'
    img2 = './test/img/mihotel.jpg'
    img3 = './test/img/bird.jpg'
    frame1 = cv2.imread(img1)
    frame2 = cv2.imread(img2)
    frame3 = cv2.imread(img3)
    print(detector.get_color(frame1), detector.get_color(frame2), detector.get_color(frame3))
    # Expected output: red white cyan
