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
        self.direction_list = ['left', 'path']
        # camera frames are received from the main process, so set a default value here
        self.cameras = []
        for i in range(2):
            self.cameras.append(robot.getCamera(self.direction_list[i] + '_cam'))
            self.cameras[i].enable(timestep)
        # compass for moving direction
        self.compass = robot.getCompass('compass')
        self.compass.enable(timestep)
        # GPS for position and speed
        self.gps = robot.getGPS('gps')
        self.gps.enable(timestep)
        self.beacon = ''
        self.tank = ''

    def update(self):
        '''
        get and return `gpsRaw_position`, `gpsRaw_speed`, `compassRaw`, `camerasRaw`
        '''
        gpsRaw_position = self.gps.getValues()
        gpsRaw_speed = self.gps.getSpeed()
        compassRaw = self.compass.getValues()
        camerasRaw = [item.getImageArray() for item in self.cameras]
        return (
            gpsRaw_position,
            gpsRaw_speed,
            compassRaw,
            camerasRaw
        )


class Detector(object):
    """
    Detector class
    """

    def __init__(self):
        self.signals = {
            'Position': [],
            'Direction_x': [],
            'Direction_-z': [],
            'Speed': [],
            'Color': [],
            'Path_Direction': [],
            'Bridge_Detection': False,
            'Gate_Detection': False
        }

        self.gpsRaw_position = [0, 0, 0]
        self.gpsRaw_speed = [0, 0, 0]
        self.compassRaw = [1, 0, 0]
        self.camerasRaw = [np.zeros((128, 128, 3), np.uint8) for i in range(4)]

        self.color_list = [
            ('red', np.array([0, 246, 144]), np.array([3, 255, 154])),
            ('orange', np.array([14, 199, 234]), np.array([21, 208, 240])),
            ('yellow', np.array([27, 243, 168]), np.array([33, 255, 178])),
            ('green', np.array([55, 236, 156]), np.array([63, 255, 173])),
            ('purple', np.array([132, 43, 46]), np.array([155, 255, 255]))
        ]

        self.foresight_up = 40
        self.foresight_down = 30
        self.chassis_front = 50
        self.front_wheels_y = 75

        info('Sensor initialed')

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

    def get_color(self, image):
        '''
        Detect the interested colors\n
        `param image`: Input image\n
        `return image_gray`: gray image with unwanted color filtered\n
        '''
        GaussianBlur = cv2.GaussianBlur(image, (5, 5), 0)  # smooth the image
        image_hsv = cv2.cvtColor(GaussianBlur, cv2.COLOR_BGR2HSV)  # cvt rgb to hsv
        color = None
        color_thresh = 20
        for item in self.color_list:
            mask = cv2.inRange(image_hsv, item[1], item[2])  # set regions of other colors to black
            binary = cv2.dilate(mask, None, iterations=2)
            sum = np.sum(binary)
            if sum > color_thresh:
                color = item[0]
                image_binary = binary
        if color == "orange":
            self.tank = 'tank'
        elif color == "green":
            self.beacon = 'after bridge'
        elif color is None:
            image_gray = cv2.cvtColor(GaussianBlur, cv2.COLOR_BGR2GRAY)
        else:
            image_gray = cv2.threshold(image_binary, 127, 255, cv2.THRESH_BINARY_INV)[1]  # Inverse the binary image
        return image_gray

    def tri2angle(self, opposite, adjacent):
        '''
        return an angle (in degrees) based on the given opposite edge and adjacent edge of
        a triangle, in range of (-180, 180]\n
        `opposite`: opposite edge of the angle\n
        `adjacent`: adjacent edge of the angle\n
        '''
        if adjacent == 0.0:
            angle = np.sign(opposite) * 90
        else:
            angle = 180 * np.arctan(opposite / adjacent) / np.pi
            if adjacent < 0:
                if opposite > 0:
                    angle = angle + 180
                else:
                    angle = angle - 180
        return angle

    def path_detection(self, image_gray):
        '''
        This algorithm gives the angle (in degrees) of the direction of the path
        if no path is detected, `None` is returned\n
        Written by Wen Bo
        '''
        cv2.waitKey(1)
        roi = image_gray[self.chassis_front - self.foresight_up:self.chassis_front - self.foresight_down]
        # cv2.imshow('roi', roi)
        threshold = 70
        location = np.argwhere((roi) <= threshold)
        if location.size == 0:
            return None
        else:
            # get center of road in roi
            f_y, f_x = np.mean(a=location, axis=0)
            return self.tri2angle(f_x - int(image_gray.shape[1] / 2), 102 - self.front_wheels_y)

    def bridge_detection(self, image_gray):
        '''
        This algorithm gives whether we detect the bridge\n
        if bridge is detected, return `True`, else return `false`
        Written by Wen Bo, modified by Han Haoran
        '''
        # Binarization
        binary_map = np.zeros(shape=image.shape)
        binary_map[image < 149] = 1
        binary_map[image > 153] = 1
        # delete the noise
        kernel = np.ones([5, 5], np.uint8)
        erosion = cv2.erode(binary_map, kernel, iterations=1)

        counter = np.sum(binary_map == 0)
        # if the x index of the bridge is in no farther than x_range*width from the center,
        # then the bridge is in the center
        if counter > 100:
            location = np.argwhere(binary_map == 0)
            f_x = np.mean(a=location, axis=0)[1]
            x_range = 0.02
            if np.abs(f_x - image.shape[1] // 2) <= x_range * binary_map.shape[1]:
                return True
        return False

    def gate_detection(self, image_gray):
        '''
        This algorithm gives whether we detect the gate\n
        if gate is detected, return `True`, else return `false`
        Written by Wen Bo, modified by Han Haoran
        '''
        # Get the  gradient map
        gradient = cv2.Sobel(image_gray, cv2.CV_64F, 1, 0, ksize=3)
        # Binarization
        binary_map = np.zeros(shape=image_gray.shape)
        binary_map[gradient > 400] = 1
        # Counting the pixel along a column where the gradient exceed the threshold
        counter = np.sum(binary_map, axis=0)
        edge = np.argwhere(counter > 10)
        if edge.shape[0] >= 4:
            f_x = np.mean(edge)
            x_range = 0.02
            if np.abs(f_x - image_gray.shape[1] // 2) <= x_range * binary_map.shape[1]:
                return True

        return False

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
                    self.capture(1)

                # update sensors data
                self.update()
                # update signals
                self.signals['time'] = time.strftime("%H:%M:%S", time.localtime())

                self.signals['Position'] = np.array(self.gpsRaw_position)
                self.signals['Direction_x'] = self.tri2angle(self.compassRaw[1], self.compassRaw[0])
                self.signals['Direction_-z'] = self.tri2angle(self.compassRaw[0], -self.compassRaw[1])
                self.signals['Speed'] = np.array(self.gpsRaw_speed)
                self.signals['Color'] = self.get_color(self.get_image(1))
                # if signals['Path_Direction']==None: the path is end
                self.signals['Path_Direction'] = self.path_detection(self.get_image(1))

                image_gray = cv2.cvtColor(self.get_image(0), cv2.COLOR_BGR2GRAY)
                if not self.signals['Bridge_Detection']:
                    self.signals['Bridge_Detection'] = self.bridge_detection(image_gray)
                if not (self.signals['Gate_Detection']) and (self.signals['Bridge_Detection']) :
                    self.signals['Gate_Detection'] = self.gate_detection(image_gray)
                # send all signals to decider
                self.send_signals(self.signals)
                # detectedInfo('\n        '.join([str(item) + ': ' + str(self.signals[item]) for item in self.signals]))


if __name__ == "__main__":
    pass
