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
            self.send_command('Turn' + str(self.signals['Path_Direction']))
        return 'line patrol'

    def lineless_x_axis(self):
        '''
        无线直行x轴
        '''
        self.send_command('Turn' + str(self.signals['Direction_x']))

    def lineless_z_axis(self):
        '''
        无线直行-z轴
        '''
        self.send_command('Turn' + str(self.signals['Direction_-z']))

    def cross_bridge(self):
        '''
        过桥逻辑
        无线直行 (结束:左侧摄像头中心线对准桥)
        转弯, (应该判定是:前摄像头与桥中心线对齐) (但是如没有对齐, 应考虑补救措施）
        无线直行 (结束: 检测到信标结束)
        右转 (start: 检测到信标)
        无线直行 (结束: 左摄像头与门的中心线对齐)
        '''
        self.lineless_x_axis()
        # 此处缺个转弯，明天与视觉组商定
        self.lineless_z_axis()
        self.send_command(self.command['2'] + ' Angle:' + self.signals['Path_Direction'])

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
