from colored import commandInfo, debugInfo, detectedInfo, info


class Decider(object):
    '''
    Decider class
    '''
    def __init__(self):
        info('Decision initialed')

    def run(self, signal_queue, command_queue):
        '''
        `signal_queue`: queue for signals from sensor\n
        `command_queue`: queue for commands to send to chassis
        '''
        while True:
            if not signal_queue.empty():
                self.detected = signal_queue.get(True)
                detectedInfo('time:' + str(self.detected))
                command_queue.put('move straight forward')


if __name__ == "__main__":
    pass
