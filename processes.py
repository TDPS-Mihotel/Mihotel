import multiprocessing
import os
import time

import chassis
import decision
import sensor
from colored import debugInfo, detectedInfo, info, movementInfo

# flags
flag_finish_patio = 0


# define the processes
def move(movement_queue):
    rover = chassis.Chassis()
    while True:
        if not movement_queue.empty():
            rover.set_state(movement_queue.get())


def sense(sense_queue):
    detector = sensor.Sensor()
    detector.run(sense_queue)


def decide(sense_queue, move_queue):
    decider = decision.Decision()
    decider.run(sense_queue, move_queue)


start = time.time()
info('start at:' + str(start))
# create pipes
move_queue = multiprocessing.Queue()
sense_queue = multiprocessing.Queue()

# create processes and start them
move_process = multiprocessing.Process(target=move, args=(move_queue, ))
sense_process = multiprocessing.Process(target=sense, args=(sense_queue, ))
decide_process = multiprocessing.Process(target=decide, args=(sense_queue, move_queue,))
move_process.daemon = True
sense_process.daemon = True
decide_process.daemon = True
move_process.start()
sense_process.start()
decide_process.start()

while True:
    # now use time to be finish flag signal
    if time.time() - start > 1:  # 1s
        flag_finish_patio = 1
    if flag_finish_patio:
        break
info('time period:' + str(time.time() - start))
