import time

from colored import commandInfo, debugInfo, detectedInfo, info


class MotorsGroup(object):
    '''
    rover motor interface
    '''

    def __init__(self):
        pass

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

        timestep = int(robot.getBasicTimeStep())

        # enable motors
        self.motors = {}
        # self.motors['arm'] = robot.getMotor('arm')
        # wheel
        self.motors['wheel1'] = robot.getMotor('wheel1')
        self.motors['wheel2'] = robot.getMotor('wheel2')
        self.motors['wheel3'] = robot.getMotor('wheel3')
        self.motors['wheel4'] = robot.getMotor('wheel4')
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
<<<<<<< Updated upstream
        self.velocityDict = {}
=======
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
>>>>>>> Stashed changes
        info('Chassis initialed')

    def set_queue(self, command_queue, motors_queue):
        self.command_queue = command_queue
        self.motors_queue = motors_queue

    def recv_command(self):
        '''
        return the received command from command_queue\n
        the return value will be `''` if command_queue is empty
        '''
        while not self.command_queue.empty():
            return self.command_queue.get()
        else:
            return ''

    def set_state(self, command):
        '''
        set state of the chassis by command, a commandInfo will output
        '''
        # clean state
        for motor in self.velocityDict:
            self.velocityDict[motor] = 0

        if command:
<<<<<<< Updated upstream
            if command == 'Move forward':
                self.state = 'Moving forward'
                self.velocityDict['wheel1'] = -10
                self.velocityDict['wheel2'] = -10
                self.velocityDict['wheel3'] = -10
                self.velocityDict['wheel4'] = -10

            if command == 'Move backward':
                self.state = 'Moving backward'
                self.velocityDict['wheel1'] = 10
                self.velocityDict['wheel2'] = 10
                self.velocityDict['wheel3'] = 10
                self.velocityDict['wheel4'] = 10

            if command == 'Turn right':
                self.state = 'Turning right'
                self.velocityDict['wheel1'] = -10
                self.velocityDict['wheel2'] = -10
                self.velocityDict['wheel3'] = 10
                self.velocityDict['wheel4'] = 10

            if command == 'Turn left':
                self.state = 'Turning left'
                self.velocityDict['wheel1'] = 10
                self.velocityDict['wheel2'] = 10
                self.velocityDict['wheel3'] = -10
                self.velocityDict['wheel4'] = -10
=======
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
>>>>>>> Stashed changes

            if command == 'Stop':
                self.state = 'Stopped'
                self.velocityDict['wheel1'] = -10
                self.velocityDict['wheel2'] = -10
                self.velocityDict['wheel3'] = -10
                self.velocityDict['wheel4'] = -10

            self.motors_queue.put(self.velocityDict)
            commandInfo(self.state)

    def run(self, flag_pause):
        '''
        `flag_pause`: the flag to pause this Decider running (actually skips all code in this function)\n
        '''
        while True:
            # time.sleep(0.1)  # set chassis period to 0.1s
            # skip all code inside if paused by webots
            if not flag_pause.value:
                self.set_state(self.recv_command())


if __name__ == "__main__":
    pass
