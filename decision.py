from colored import commandInfo, debugInfo, detectedInfo, info


class Decider(object):
    '''
    Decider class
    '''

    def __init__(self):
        info('Decision initialed')

    def run(self, signal_queue, command_queue, flag_pause, lock):
        '''
        `signal_queue`: queue for signals from sensor\n
        `command_queue`: queue for commands to send to chassis\n
        `flag_pause`: the flag to pause this Decider running (actually skip all
            code in this function)\n
        `lock`: a process lock, used for `flag_pause`
        '''
        while True:
            if not (signal_queue.empty() or flag_pause.value):
                self.detected = signal_queue.get(True)
                command_queue.put('move straight forward')
                with lock:
                    flag_pause.value = True


if __name__ == "__main__":
    pass
