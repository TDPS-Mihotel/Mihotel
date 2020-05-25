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
        self.direction_list = ['right', 'left', 'path']
        # camera frames are received from the main process, so set a default value here
        self.cameras = []
        for i in range(3):
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
            'Bridge_Detection': []
        }

        self.gpsRaw_position = [0, 0, 0]
        self.gpsRaw_speed = [0, 0, 0]
        self.compassRaw = [1, 0, 0]
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

        self.foresight_up = 40
        self.foresight_down = 30
        self.chassis_front = 50
        self.front_wheels_y = 75

        self.window_edge = 9
        self.window_h_size = int((self.window_edge - 1) / 2)
        self.adjacent_num = 30

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
                ) = self.sensors_queue.get(block=False)
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

    def path_detection(self, image):
        '''
        This algorithm gives the angle (in degrees) of the direction of the path
        if no path is detected, `None` is returned\n
        Written by Wen Bo
        '''
        cv2.waitKey(1)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        roi = image_gray[self.chassis_front - self.foresight_up:self.chassis_front - self.foresight_down]
        # cv2.imshow('gray', roi)
        threshold = 70
        location = np.argwhere((roi) <= threshold)
        if location.size == 0:
            return None
        else:
            # get center of road in roi
            f_y, f_x = np.mean(a=location, axis=0)
            return self.tri2angle(f_x - int(image.shape[1] / 2), 102 - self.front_wheels_y)

    def bridge_detection(self, image):
        '''
        This algorithm gives the angle (in degrees) of the direction of the path
        if no path is detected, `None` is returned\n
        Written by Wen Bo
        '''
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Binarization
        binary_map = np.zeros(shape=image_gray.shape)
        binary_map[image_gray < 149] = 1
        binary_map[image_gray > 153] = 1
        # delete the noise
        kernel = np.ones([5, 5], np.uint8)
        erosion = cv2.erode(binary_map, kernel, iterations=1)

        instruction = False
        counter = np.sum(binary_map == 0)
        # if the x index of the bridge is in [63,65], the the bridge is in the center
        if counter > 100:
            location = np.argwhere(binary_map == 0)
            f_x = np.mean(a=location, axis=0)[1]
            mid = binary_map.shape[1] / 2
            x_range = 0.02
            if np.abs(f_x - mid) <= x_range * binary_map.shape[1]:
                instruction = True
                print(f_x, instruction)
        return instruction

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
                    self.capture(2)

                # update sensors data
                self.update()
                # update signals
                self.signals['time'] = time.strftime("%H:%M:%S", time.localtime())

                self.signals['Position'] = np.array(self.gpsRaw_position)
                self.signals['Direction_x'] = self.tri2angle(self.compassRaw[1], self.compassRaw[0])
                self.signals['Direction_-z'] = self.tri2angle(self.compassRaw[0], -self.compassRaw[1])
                self.signals['Speed'] = np.array(self.gpsRaw_speed)
                self.signals['Color'] = self.get_color(self.get_image(2))
                # if signals['Path_Direction']==None: the path is end
                self.signals['Path_Direction'] = self.path_detection(self.get_image(2))
                self.signals['Bridge_Detection'] = self.bridge_detection(self.get_image(1))

                # send all signals to decider
                self.send_signals(self.signals)
                # detectedInfo('\n        '.join([str(item) + ': ' + str(self.signals[item]) for item in self.signals]))


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
