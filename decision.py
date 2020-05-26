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
        self.states = {
            'line patrol': self.line_patrol,
            'stop': self.stop,
            'cross_bridge': self.cross_bridge,
            'cross_gate': self.cross_gate
        }
        self.current_state = 'line patrol'
        info('Decision initialed')

# ############################# state functions ################################
    def line_patrol(self):
        '''
        巡线
        '''
        # 在程序刚开始时可能这个量还没有传过来, 所以先判断下有没有
        if 'Path_Direction' in self.signals:
            if self.signals['Path_Direction'] is None:
                return 'stop'
            if self.signals['feed'] is True:
                pass
            self.send_command('Turn' + str(self.signals['Path_Direction']))
        return 'line patrol'

    def cross_bridge(self):
        '''
        过桥逻辑
        '''
        if self.signals['Bridge_Detection'] is False and self.signals['Gate_Detection'] is False:
            # 过桥前直行x
            self.send_command('Turn' + str(self.signals['Direction_x']))
            return 'cross_bridge'
        elif self.signals['Bridge_Detection'] is True and self.signals['Gate_Detection'] is False:
            # 对准桥转向-z直行
            self.send_command('Turn' + str(self.signals['Direction_-z']))
            return 'cross_bridge'
        elif self.signals['Color'] == 'Green':
            # 过桥后左转，切换状态
            self.send_command('Turn' + str(self.signals['Direction_x']))
            self.send_command('Stop')
            return 'cross_gate'

    def cross_gate(self):
        '''
        过门
        '''
        if self.signals['Bridge_Detection'] is True and self.signals['Gate_Detection'] is False:
            # 过门前直行x
            self.send_command('Turn' + str(self.signals['Direction_x']))
            return 'cross_gate'
        elif self.signals['Bridge_Detection'] is True and self.signals['Gate_Detection'] is True:
            # 对准门转向-z直行
            self.send_command('Turn' + str(self.signals['Direction_-z']))
            return 'cross_gate'
        elif self.signals['Path_Direction'] is not None:
            # 过门后，切换巡线状态
            self.send_command('Stop')
            return 'line patrol'

    def stop(self):
        '''
        测试用
        '''
        self.send_command('Stop')
        return 'stop'

# ############################ state functions end #############################

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
                self.signals = self.signal_queue.get(block=True, timeout=0.05)
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

        self.current_state = self.states[self.current_state]()


if __name__ == "__main__":
    pass
