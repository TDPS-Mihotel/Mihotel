from colored import debugInfo, detectedInfo, info, movementInfo


class Chassis(object):
    def __init__(self):
        self.state = 'ready'
        info('Chassis initialed')

    def set_state(self, state):
        '''
        set new movement state of the chassis
        '''
        self.state = state
        movementInfo(self.state)
