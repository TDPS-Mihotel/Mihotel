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
        self.motors['arm'] = robot.getMotor('arm')
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
        self.velocityDict = {}
        self.defaultVelocity = 30
        self.maxVelocity = 50
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
            if command == 'Rotate arm':
                self.state = 'Arm rotating'
                self.velocityDict['arm'] = 10
            # wheel
            if command[:4] == 'Turn' and command[:5] != 'Turn ':
                shift = float(command[4:]) * 10
                self.state = command
                self.velocityDict['wheel1'] = self.defaultVelocity + shift
                self.velocityDict['wheel2'] = self.defaultVelocity + shift
                self.velocityDict['wheel3'] = self.defaultVelocity - shift
                self.velocityDict['wheel4'] = self.defaultVelocity - shift

            if command == 'Move forward':
                self.state = 'Moving forward'
                self.velocityDict['wheel1'] = self.defaultVelocity
                self.velocityDict['wheel2'] = self.defaultVelocity
                self.velocityDict['wheel3'] = self.defaultVelocity
                self.velocityDict['wheel4'] = self.defaultVelocity

            if command == 'Move backward':
                self.state = 'Moving backward'
                self.velocityDict['wheel1'] = -self.defaultVelocity
                self.velocityDict['wheel2'] = -self.defaultVelocity
                self.velocityDict['wheel3'] = -self.defaultVelocity
                self.velocityDict['wheel4'] = -self.defaultVelocity

            if command == 'Turn right':
                self.state = 'Turning right'
                self.velocityDict['wheel1'] = self.defaultVelocity
                self.velocityDict['wheel2'] = self.defaultVelocity
                self.velocityDict['wheel3'] = -self.defaultVelocity
                self.velocityDict['wheel4'] = -self.defaultVelocity

            if command == 'Turn left':
                self.state = 'Turning left'
                self.velocityDict['wheel1'] = -self.defaultVelocity
                self.velocityDict['wheel2'] = -self.defaultVelocity
                self.velocityDict['wheel3'] = self.defaultVelocity
                self.velocityDict['wheel4'] = self.defaultVelocity

            if command == 'Stop':
                self.state = 'Stopped'
                self.velocityDict['wheel1'] = 0
                self.velocityDict['wheel2'] = 0
                self.velocityDict['wheel3'] = 0
                self.velocityDict['wheel4'] = 0

            for item in self.velocityDict:
                if self.velocityDict[item] < -self.maxVelocity:
                    self.velocityDict[item] = -self.maxVelocity
                if self.velocityDict[item] > self.maxVelocity:
                    self.velocityDict[item] = self.maxVelocity
                self.velocityDict[item] = -self.velocityDict[item]

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
