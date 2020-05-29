import queue
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
        if velocityDict['Shoulder'] > 0:
            if self.arm_action == 'forward':
                # give 0.25s to rotate forward
                if self.robot.getTime() - self.time > 0.25:
                    velocityDict['Shoulder'] = 0
                    velocityDict['Elbow'] = 0
                    velocityDict['Wrist'] = 0
            else:
                self.arm_action = 'forward'
                self.time = self.robot.getTime()
        if velocityDict['Shoulder'] < 0:
            if self.arm_action == 'backward':
                # give 0.5s to rotate back
                if self.robot.getTime() - self.time > 0.5:
                    velocityDict['Shoulder'] = 0
                    velocityDict['Elbow'] = 0
                    velocityDict['Wrist'] = 0
            else:
                self.arm_action = 'backward'
                self.time = self.robot.getTime()
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
        self.defaultVelocity = 30
        self.maxVelocity = 30
        self.steer_coefficient = 0.5
        info('Chassis initialed')

    def set_queue(self, command_queue, motors_queue):
        self.command_queue = command_queue
        self.motors_queue = motors_queue

    def recv_command(self):
        '''
        return the received command from command_queue\n
        the return value will be `''` if command_queue is empty
        '''
        command = ''
        while True:
            try:
                command = self.command_queue.get(block=True, timeout=0.05)
            except queue.Empty:
                break
        return command

    def set_state(self, command):
        '''
        set state of the chassis by command, a commandInfo will output
        '''

        if command:
            if command == 'Feed':
                self.state = 'Feeding'
                self.velocityDict['Shoulder'] = 8
                # self.velocityDict['Elbow'] = 0
                self.velocityDict['Wrist'] = -15

            if command == 'Feeder recover':
                self.state = 'Feeder recovering'
                self.velocityDict['Shoulder'] = -4
                # self.velocityDict['Elbow'] = 0
                self.velocityDict['Wrist'] = 7.5

            # wheel
            if command[:4] == 'Turn':
                steer = float(command[4:]) * self.steer_coefficient
                self.state = 'Steering speed: ' + str(steer)
                self.velocityDict['flWheel'] = self.defaultVelocity + steer
                self.velocityDict['rlWheel'] = self.defaultVelocity + steer
                self.velocityDict['rrWheel'] = self.defaultVelocity - steer
                self.velocityDict['frWheel'] = self.defaultVelocity - steer

            if command == 'Move forward':
                self.state = 'Moving forward'
                self.velocityDict['flWheel'] = self.defaultVelocity
                self.velocityDict['rlWheel'] = self.defaultVelocity
                self.velocityDict['rrWheel'] = self.defaultVelocity
                self.velocityDict['frWheel'] = self.defaultVelocity

            if command == 'Move backward':
                self.state = 'Moving backward'
                self.velocityDict['flWheel'] = -self.defaultVelocity
                self.velocityDict['rlWheel'] = -self.defaultVelocity
                self.velocityDict['rrWheel'] = -self.defaultVelocity
                self.velocityDict['frWheel'] = -self.defaultVelocity

            if command == 'Stop':
                self.state = 'Stopped'
                self.velocityDict['flWheel'] = 0
                self.velocityDict['rlWheel'] = 0
                self.velocityDict['rrWheel'] = 0
                self.velocityDict['frWheel'] = 0

            # wheel motor speed limitation and reverse
            for motor in self.velocityDict:
                if 'Wheel' in motor:
                    if self.velocityDict[motor] < -self.maxVelocity:
                        self.velocityDict[motor] = -self.maxVelocity
                    if self.velocityDict[motor] > self.maxVelocity:
                        self.velocityDict[motor] = self.maxVelocity
                    self.velocityDict[motor] = -self.velocityDict[motor]

            self.motors_queue.put(self.velocityDict)
            # commandInfo(self.state)

    def run(self, flag_pause):
        '''
        `flag_pause`: the flag to pause this Decider running (actually skips all code in this function)\n
        '''
        while True:
            time.sleep(0.1)  # set chassis period to 0.1s
            self.set_state(self.recv_command())
            # commandInfo(self.state)


if __name__ == "__main__":
    pass
