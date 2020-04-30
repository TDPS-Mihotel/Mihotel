import time
from colored import commandInfo, debugInfo, detectedInfo, info


class Decider(object):
    '''
    Decider class
    '''

    def __init__(self, flag_patio_finished):
        self.flag_patio_finished = flag_patio_finished
        self.signals = {}
        info('Decision initialed')

    def set_queues(self, signal_queue, command_queue):
        '''
        `signal_queue`: queue for signals from sensor\n
        `command_queue`: queue for commands to send to chassis\n
        '''
        self.signal_queue = signal_queue
        self.command_queue = command_queue

    def send_command(self, command):
        self.command_queue.put(command)

    def update_signals(self):
        '''
        update self.signals if signal_queue is not empty
        '''
        if not self.signal_queue.empty():
            self.signals = self.signal_queue.get()

    def run(self, flag_pause, key, lock):
        '''
        `flag_pause`: the flag to pause this Decider running (actually skips all code in this function)\n
        'key': a dict containing character of keyboard key press\n
        `lock`: a process lock, used for `flag_pause`\n
        '''
        while True:
            time.sleep(0.1)  # set decision period to 0.1s
            # skip all code inside if paused by webots
            if not flag_pause.value:
                # decision group's code goes under this ########################
                if key.value == ord('Q'):
                    debugInfo('Quit')
                    with lock:
                        self.flag_patio_finished.value = True

                self.update_signals()
                self.send_command('move straight forward')
                # decision group's code ends ###################################
                # keep this at the end of run()
                with lock:
                    flag_pause.value = True


if __name__ == "__main__":
    pass
