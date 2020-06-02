import time
from colored import commandInfo, debugInfo, stateInfo, detectedInfo, info


class Decider(object):
    '''
    Decider class
    '''

    def __init__(self):
        self.flag_patio_finished = False
        self.signals = {}
        self.states = {
            'line_patrol': self.line_patrol,
            'stop': self.stop,
            'cross_bridge': self.cross_bridge,
            'cross_gate': self.cross_gate,
        }
        self.current_state = 'line_patrol'
        self.lost_count = 0
        self.last_turn = 0
        self.isFeeded = False
        info('Decision initialed')
        stateInfo(self.current_state)

# ############################# state functions ################################
    def line_patrol(self):
        '''
        巡线
        '''
        if self.signals['Path_Direction'] is None:
            if self.lost_count > 5:
                if self.signals['Path_color'] is None:
                    # 转过桥状态
                    stateInfo('cross_bridge')
                    return 'cross_bridge'
                else:
                    # 终点无线stop
                    commandInfo('Stop')
                    stateInfo('Finish')
                    return 'stop'
            else:
                self.lost_count += 1
                self.send_command('Turn' + str(self.last_turn))
                debugInfo('Path lost count:' + str(self.lost_count))
                return 'line_patrol'
        if self.signals['Beacon'] == 'tank' and not self.isFeeded:
            # 橙盒子投食
            self.send_command('Feed')
            self.isFeeded = True
            return 'line_patrol'
        # 巡黑线或彩色线
        self.send_command('Turn' + str(self.signals['Path_Direction']))
        self.lost_count = 0
        self.last_turn = self.signals['Path_Direction']
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

    def send_command(self, command):
        self.command = command

    def state_machine(self):
        '''
        '''
        self.current_state = self.states[self.current_state]()


if __name__ == "__main__":
    pass
