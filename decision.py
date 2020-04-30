import time
from colored import commandInfo, debugInfo, detectedInfo, info


class Decider(object):
    '''
    Decider class
    '''

    def __init__(self, flag_patio_finished):
        self.flag_patio_finished = flag_patio_finished
        info('Decision initialed')

    def run(self, signal_queue, command_queue, flag_pause, key, lock):
        '''
        `signal_queue`: queue for signals from sensor\n
        `command_queue`: queue for commands to send to chassis\n
        `flag_pause`: the flag to pause this Decider running (actually skip all
            code in this function)\n
        'key': a dict containing character of keyboard key press
        `lock`: a process lock, used for `flag_pause`
        '''
        while True:
            time.sleep(0.01)
            if not (signal_queue.empty() or flag_pause.value):
                self.detected = signal_queue.get(True)
                command_queue.put('move straight forward')
                with lock:
                    flag_pause.value = True
                if key.value == ord('Q'):
                    debugInfo('Quit')
                    with lock:
                        self.flag_patio_finished.value = True


if __name__ == "__main__":
    pass
