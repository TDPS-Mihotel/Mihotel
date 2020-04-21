from colored import debugInfo, detectedInfo, info, movementInfo


class Decision(object):
    def __init__(self):
        self.state = ''
        info('Decision initialed')

    def run(self, sense_queue, move_queue):
        while True:
            if not sense_queue.empty():
                self.detected = sense_queue.get(True)
                detectedInfo('time:' + str(self.detected))
                move_queue.put('moving straight forward')
