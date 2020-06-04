import time

from colored import commandInfo, debugInfo, detectedInfo, info


class MotorsGroup(object):
    '''
    rover motor interface
    '''

    def __init__(self):
        self.motors = {}

    def update(self, velocityDict):
        '''
        `velocityList`: list of velocity to set to motors
        '''
        for motor in velocityDict:
            self.motors[motor].setVelocity(velocityDict[motor])


class WebotsMotorsGroup(MotorsGroup):
    '''
    webots rover motor interface
    '''

    def __init__(self, robot):
        super().__init__()

        self.robot = robot
        self.time = robot.getTime()
        self.arm_action = ''

        timestep = int(robot.getBasicTimeStep())

        # arm
        self.motors['Shoulder'] = robot.getMotor('Shoulder')
        self.motors['Elbow'] = robot.getMotor('Elbow')
        self.motors['Wrist'] = robot.getMotor('Wrist')
        # wheel
        self.motors['flWheel'] = robot.getMotor('flWheel')
        self.motors['rlWheel'] = robot.getMotor('rlWheel')
        self.motors['rrWheel'] = robot.getMotor('rrWheel')
        self.motors['frWheel'] = robot.getMotor('frWheel')
        for motor in self.motors:
            self.motors[motor].setPosition(float('inf'))
            self.motors[motor].setVelocity(0.0)

    def update(self, velocityDict):
        return super().update(velocityDict)


class Controller(object):
    '''
    chassis controller
    '''

    def __init__(self):
        self.velocityDict = {
            'flWheel': 0,
            'frWheel': 0,
            'rlWheel': 0,
            'rrWheel': 0,
            'Shoulder': 0,
            'Elbow': 0,
            'Wrist': 0,
        }
        self.state = ''
        self.feed_action = False
        # parameters
        self.maxVelocity = 45
        self.defaultVelocity = 45
        self.steer_coefficient = 0.5
        self.feed_time = 0.3  # in seconds
        self.flag = 0
        self.timerecord = 0
        info('Chassis initialed')

    def set_state(self, command, time):
        '''
        set state of the chassis by command, a commandInfo will output
        '''

        if command:
            if command == 'Feed' or self.feed_action or (self.flag > 0):
                self.state = 'Feeding'
                shoulder_vel = 5
                elbow_vel = 0
                wrist_vel = 8

                if self.flag == 0:
                    self.timerecord = time
                    self.flag = 1
                if time - self.timerecord > 0.3:
                    self.flag = 2

                if (self.feed_action is False) and (self.flag == 2):
                    self.velocityDict['flWheel'] = 0
                    self.velocityDict['rlWheel'] = 0
                    self.velocityDict['rrWheel'] = 0
                    self.velocityDict['frWheel'] = 0
                    self.velocityDict['Shoulder'] = shoulder_vel
                    self.velocityDict['Elbow'] = elbow_vel
                    self.velocityDict['Wrist'] = -wrist_vel
                    self.feed_action = True
                    self.feed_start = time
                    commandInfo(self.state)
                elif(self.flag == 2):
                    if time - self.feed_start < self.feed_time:
                        pass
                    elif time - self.feed_start < self.feed_time * 3:
                        self.velocityDict['Shoulder'] = 0
                        self.velocityDict['Elbow'] = 0
                        self.velocityDict['Wrist'] = 0
                    elif time - self.feed_start < self.feed_time * 5:
                        self.velocityDict['Shoulder'] = -shoulder_vel / 1.8
                        self.velocityDict['Elbow'] = -elbow_vel / 1.8
                        self.velocityDict['Wrist'] = wrist_vel / 1.8
                    else:
                        self.velocityDict['Shoulder'] = 0
                        self.velocityDict['Elbow'] = 0
                        self.velocityDict['Wrist'] = 0
                        commandInfo('Feeder recovered')
                        self.feed_action = False
                        self.flag = 0

            # wheel
            if command[:4] == 'Turn' and (self.feed_action is False):
                steer = float(command[4:]) * self.steer_coefficient
                self.state = 'Steering speed: ' + str(steer)
                self.velocityDict['flWheel'] = self.defaultVelocity + steer
                self.velocityDict['rlWheel'] = self.defaultVelocity + steer
                self.velocityDict['rrWheel'] = self.defaultVelocity - steer
                self.velocityDict['frWheel'] = self.defaultVelocity - steer
                # wheel motor speed limitation and reverse
                for motor in self.velocityDict:
                    if 'Wheel' in motor:
                        if self.velocityDict[motor] < -self.maxVelocity:
                            self.velocityDict[motor] = -self.maxVelocity
                        if self.velocityDict[motor] > self.maxVelocity:
                            self.velocityDict[motor] = self.maxVelocity
                        self.velocityDict[motor] = -self.velocityDict[motor]
            if command == 'Stop':
                self.state = 'Stopped'
                self.velocityDict['flWheel'] = 0
                self.velocityDict['rlWheel'] = 0
                self.velocityDict['rrWheel'] = 0
                self.velocityDict['frWheel'] = 0

            # commandInfo(self.state)


if __name__ == "__main__":
    pass
