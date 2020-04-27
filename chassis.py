# TODO: fix colored
from colored import commandInfo, debugInfo, detectedInfo, info


class Controller(object):
    '''
    Controller class
    '''
    def __init__(self):
        info('Chassis initialed')

    def set_state(self, command):
        '''
        set state of the chassis by command, a commandInfo will output
        '''
        self.state = command
        commandInfo(self.state)


if __name__ == "__main__":
    pass
