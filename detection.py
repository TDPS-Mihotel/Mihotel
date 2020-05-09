import time
import queue
import cv2
import numpy as np

from colored import commandInfo, debugInfo, detectedInfo, info

from controller import Robot,Camera,Compass,GPS,DistanceSensor

class Detector(object):
    """
    Detector class
    """

    def __init__(self):
        
        #Path_Dirction is waiting for Wen Bo
        #Later, various Object_Dectection could be added 
        self.signals = {}
        self.signal_queue=queue.Queue()
        
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

        self.direction_list=['front','right','left']

        #for each dirction, there are three distance sensors
        self.distance_sensor=[[],[],[]]
        for i in range(3):
            for j in range(3):
                self.distance_sensor[i].append(DistanceSensor(self.direction_list[i]+'_'+self.direction_list[j]))
                self.distance_sensor[i][j].enable(1)

        #one camera for each direction, one camera specific for path detection
        self.camera = []
        for i in range(3):
            self.camera.append(Camera(self.direction_list[i]))
            self.camera[i].enable(1)
        self.camera.append(Camera('path'))
        self.camera[3].enable(1)

        #compass for moving direction
        self.compass=Compass('compass')
        self.compass.enable(1)

        #GPS for position and speed
        self.gps=GPS('gps')
        self.gps.enable(1)

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

    def capture(self, index):
        '''
        capture images from camera to test/camera/
        '''
        image = np.array(self.camera[index].getImageArray(), dtype="uint8")
        r, g, b = cv2.split(image)
        image = cv2.merge([b, g, r])
        return image

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
                    cv2.imwrite("D:\Image.PNG", self.capture(0))

                # update signals
                self.signals['time (min)'] = time.localtime(time.time()).tm_min
                self.signals['Position'] = np.array(self.gps.getValues())
                self.signals['Direction'] = np.array(self.compass.getValues())
                self.signals['Speed'] = np.array(self.gps.getSpeed())
                # the minimum distance for each direction where the unit is m.
                self.signals['Front_Distance'] = np.min([self.distance_sensor[0][0].getValue(),
                                                         self.distance_sensor[0][1].getValue(),
                                                         self.distance_sensor[0][2].getValue()]) / 1000
                self.signals['Right_Distance'] = np.min([self.distance_sensor[1][0].getValue(),
                                                         self.distance_sensor[1][1].getValue(),
                                                         self.distance_sensor[1][2].getValue()]) / 1000
                self.signals['Left_Distance'] = np.min([self.distance_sensor[2][0].getValue(),
                                                        self.distance_sensor[2][1].getValue(),
                                                        self.distance_sensor[2][2].getValue()]) / 1000
                self.signals['Color'] = self.get_color(self.capture(3))
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
