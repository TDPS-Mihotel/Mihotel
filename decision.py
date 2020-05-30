import queue
import time
from colored import commandInfo, debugInfo, stateInfo, detectedInfo, info


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
                if len(self.signals):
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
            'line_patrol': self.line_patrol,
            'stop': self.stop,
            'cross_bridge': self.cross_bridge,
            'cross_gate': self.cross_gate,
        }
        self.current_state = 'line_patrol'
        self.lost_count = 0
        self.isFeeded = False
        info('Decision initialed')
        stateInfo(self.current_state)

# ############################# state functions ################################
    def line_patrol(self):
        '''
        巡线
        '''
        if self.signals['Path_Direction'] is None:
            if self.lost_count > 9:
                if not self.signals['Bridge_Detection']:
                    # 无线收机械臂，转过桥状态
                    self.send_command('Feeder recover')
                    commandInfo('Feeder recover')
                    stateInfo('cross_bridge')
                    return 'cross_bridge'
                else:
                    # 终点无线stop
                    commandInfo('Stop')
                    stateInfo('Finish')
                    return 'stop'
            else:
                self.lost_count += 1
                self.send_command('Turn0')
                debugInfo('Path lost count:' + str(self.lost_count))
                return 'line_patrol'
        if self.signals['Beacon'] == 'tank' and not self.isFeeded:
            # 橙盒子投食
            self.send_command('Feed')
            commandInfo('Feed')
            self.isFeeded = True
            return 'line_patrol'
        # 巡黑线或彩色线
        self.send_command('Turn' + str(self.signals['Path_Direction']))
        self.lost_count = 0
        return 'line_patrol'

    def cross_bridge(self):
        '''
        过桥逻辑
        '''
        if not self.signals['Bridge_Detection']:
            # 过桥前直行x
            self.send_command('Turn' + str(-self.signals['Direction_x']))
            return 'cross_bridge'
        else:
            if self.signals['Beacon'] == 'after bridge':
                # 过桥后切换过门状态
                stateInfo('cross_gate')
                return 'cross_gate'
            # 对准桥左转向-z直行
            self.send_command('Turn' + str(-self.signals['Direction_-z']))
            return 'cross_bridge'

    def cross_gate(self):
        '''
        过门
        '''
        if not self.signals['Gate_Detection']:
            # 过门前直行x
            self.send_command('Turn' + str(-self.signals['Direction_x']))
            return 'cross_gate'
        else:
            if self.signals['Path_Direction']:
                # 过门后切换巡线状态
                self.send_command('Turn' + str(self.signals['Path_Direction']))
                stateInfo('line_patrol')
                return 'line_patrol'
            # 对准门左转向-z直行
            self.send_command('Turn' + str(-self.signals['Direction_-z']))
            return 'cross_gate'

    def stop(self):
        '''
        End
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
        while True:
            if self.command_queue.empty():
                self.command_queue.put(command)
                break

    def update_signals(self):
        '''
        update self.signals if signal_queue is not empty
        '''
        try:
            self.signals = self.signal_queue.get(block=True, timeout=0.05)
        except queue.Empty:
            pass

    @runLoop
    def state_machine(self, flag_pause, key, lock):
        '''
        `flag_pause`: the flag to pause this Decider running (actually skips all code in this function)\n
        'key': a dict containing character of keyboard key press\n
        `lock`: a process lock, used for `flag_pause`\n
        '''
        if key.value == ord('Q'):
            stateInfo('Quit manually')
            with lock:
                self.flag_patio_finished.value = True

        self.current_state = self.states[self.current_state]()


if __name__ == "__main__":
    pass
