"""Mihotel rover"""

import multiprocessing
import os
import sys
import time

import psutil


# flags ########################################################################
# flag_simulation = True  # turn to False to run for real rover
# run simulation rover if webots software is running
flag_simulation = len([p.name() for p in psutil.process_iter() if 'webots' in p.name()])
flag_patio_finished = False
flag_pause = multiprocessing.Value('i', True)


# define the processes #########################################################
def control(command_queue):
    controller = chassis.Controller()
    while True:
        if not command_queue.empty():
            controller.set_state(command_queue.get())


def detect(signal_queue, flag_pause):
    detector = detection.Detector()
    detector.run(signal_queue, flag_pause)


def decide(signal_queue, command_queue, flag_pause, lock):
    decider = decision.Decider()
    decider.run(signal_queue, command_queue, flag_pause, lock)


# import depending on simulation or not ########################################
if flag_simulation:
    os.chdir(sys.path[0])
    sys.path.append('../../../')

from colored import commandInfo, debugInfo, detectedInfo, info, logoInfo
import chassis
import decision
import detection

# program starts ###############################################################
if __name__ == "__main__":
    start = time.time()
    logoInfo()

    # create pipes
    command_queue = multiprocessing.Queue()
    signal_queue = multiprocessing.Queue()

    # create process lock
    lock = multiprocessing.Lock()

    # initial processes and set them as deamon process
    controller_process = multiprocessing.Process(target=control, args=(command_queue, ))
    detector_process = multiprocessing.Process(target=detect, args=(signal_queue, flag_pause))
    decider_process = multiprocessing.Process(target=decide, args=(signal_queue, command_queue, flag_pause, lock))
    controller_process.daemon = True
    detector_process.daemon = True
    decider_process.daemon = True
    controller_process.start()
    detector_process.start()
    decider_process.start()

# if run for webots rover
if __name__ == "__main__" and flag_simulation:
    from controller import AnsiCodes, Robot
    # create the Robot instance.
    robot = Robot()
    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        # resume decider process
        with lock:
            flag_pause.value = False

# if run for real rover
if __name__ == "__main__" and not flag_simulation:
    # when flag_patio_finished becomes True, main process ends, and all child
    # processes end with it
    while True:
        # temporarily using time to be the finish flag signal
        if time.time() - start > 2:  # 2s
            flag_patio_finished = True
        if flag_patio_finished:
            break
        with lock:
            flag_pause.value = False
    info('Finished!')
