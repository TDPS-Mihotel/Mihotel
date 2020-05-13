import time

from colored import commandInfo, debugInfo, detectedInfo, info


class Motor(object):
    '''
    motor interface
    '''
    def __init__(self, robot):
        timestep = int(robot.getBasicTimeStep())

        # enable motors
        self.motors = {}
        self.motors['arm'] = robot.getMotor('arm')
        for motor in self.motors:
            self.motors[motor].setPosition(float('inf'))
            self.motors[motor].setVelocity(0.0)

    def update(self, velocityDict):
        '''
        `velocityList`: list of velocity to set to motors
        '''
        for motor in velocityDict:
            self.motors[motor].setVelocity(velocityDict[motor])


class Controller(object):
    '''
    Controller class
    '''
    def __init__(self):
        self.velocityDict = {}
        info('Chassis initialed')

    def set_queue(self, command_queue, motors_queue):
        self.command_queue = command_queue
        self.motors_queue = motors_queue

    def recv_command(self):
        '''
        return the received command from command_queue\n
        the return value will be `''` if command_queue is empty
        '''
        if not self.command_queue.empty():
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
            self.motors_queue.put(self.velocityDict)
            commandInfo(self.state)

    def run(self, flag_pause):
        '''
        `flag_pause`: the flag to pause this Decider running (actually skips all code in this function)\n
        '''
        while True:
            time.sleep(0.1)  # set chassis period to 0.1s
            # skip all code inside if paused by webots
            if not flag_pause.value:
                self.set_state(self.recv_command())


if __name__ == "__main__":
    pass
