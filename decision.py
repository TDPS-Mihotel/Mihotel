import queue
import time
from colored import commandInfo, debugInfo, detectedInfo, info


def runLoop(state_machine):
    '''
    decorator for state_machine(), make it a loop, update signals for it
    '''

    def run(self, flag_pause, key, lock):
        while True:
            # time.sleep(0.1)  # set decision period to 0.1s
            # skip all code inside if paused by webots
            if not flag_pause.value:
                self.update_signals()
                state_machine(self, flag_pause, key, lock)
                with lock:
                    flag_pause.value = True
    return run


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
        while True:
            try:
                self.signals = self.signal_queue.get(block=False)
            except queue.Empty:
                break

    @runLoop
    def state_machine(self, flag_pause, key, lock):
        '''
        `flag_pause`: the flag to pause this Decider running (actually skips all code in this function)\n
        'key': a dict containing character of keyboard key press\n
        `lock`: a process lock, used for `flag_pause`\n
        '''
        if key.value == ord('Q'):
            debugInfo('Quit')
            with lock:
                self.flag_patio_finished.value = True

        self.send_command('Move forward')


if __name__ == "__main__":
    pass
