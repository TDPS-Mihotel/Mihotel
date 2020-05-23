"""Mihotel rover"""

import multiprocessing
import os
import queue
import sys
import time
import psutil

# flags ########################################################################
# flag_simulation = True  # turn to False to run for real rover
# run simulation rover if webots software is running
flag_simulation = len([p.name() for p in psutil.process_iter() if 'webots' in p.name()])
flag_patio_finished = multiprocessing.Value('i', False)
flag_pause = multiprocessing.Value('i', True)
key = multiprocessing.Value('i', True)

# import depending on simulation or not ########################################
if flag_simulation:
    os.chdir(sys.path[0])
    sys.path.append('../../../')

import chassis
import decision
import detection
from colored import commandInfo, debugInfo, detectedInfo, info, logoInfo


# define the processes #########################################################
def control(command_queue, motors_queue):
    controller = chassis.Controller()
    controller.set_queue(command_queue, motors_queue)
    controller.run(flag_pause)


def detect(signal_queue, flag_pause, key, sensors_queue):
    detector = detection.Detector()
    detector.set_queues(signal_queue, sensors_queue)
    detector.run(flag_pause, key)


def decide(signal_queue, command_queue, flag_pause, key, lock, flag_patio_finished):
    decider = decision.Decider(flag_patio_finished)
    decider.set_queues(signal_queue, command_queue)
    decider.state_machine(flag_pause, key, lock)


# program starts ###############################################################
if __name__ == "__main__":
    start = time.time()
    logoInfo()

    # create pipes
    command_queue = multiprocessing.Queue()
    signal_queue = multiprocessing.Queue()
    sensors_queue = multiprocessing.Queue()
    motors_queue = multiprocessing.Queue()
    queueList = [command_queue, signal_queue, sensors_queue, motors_queue]

    # create process lock
    lock = multiprocessing.Lock()

    # initial processes and set them as deamon process
    controller_process = multiprocessing.Process(target=control, args=(command_queue, motors_queue))
    detector_process = multiprocessing.Process(target=detect, args=(signal_queue, flag_pause, key, sensors_queue))
    decider_process = multiprocessing.Process(target=decide, args=(
        signal_queue, command_queue, flag_pause, key, lock, flag_patio_finished))
    controller_process.daemon = True
    detector_process.daemon = True
    decider_process.daemon = True
    controller_process.start()
    detector_process.start()
    decider_process.start()

# if run for webots rover
if __name__ == "__main__" and flag_simulation:
    from controller import Robot, Keyboard
    # create the Robot instance.
    robot = Robot()
    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())
    # enable keyboard listening
    keyboard = Keyboard()
    keyboard.enable(timestep)
    # enable sensors
    sensors = detection.Sensors(robot)
    # enable motors
    motors = chassis.WebotsMotorsGroup(robot)

    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while (robot.step(timestep) != -1) and not flag_patio_finished.value:
        # update sensors data
        sensors_queue.put(sensors.update())
        # update motors speed
        while True:
            try:
                motors.update(motors_queue.get(block=False))
            except queue.Empty:
                break
        # resume decider process
        with lock:
            flag_pause.value = False
            key.value = keyboard.getKey()  # character of the key press

# if run for real rover
if __name__ == "__main__" and not flag_simulation:
    # when flag_patio_finished becomes True, main process ends, and all child
    # processes end with it
    key.value = 1000  # it is useless for real rover now
    while not flag_patio_finished.value:
        # temporarily using time to be the finish flag signal
        if time.time() - start > 2:  # 2s
            flag_patio_finished.value = True
        with lock:
            flag_pause.value = False

if __name__ == "__main__":
    # clean up
    for queue in queueList:
        queue.close()
    info('Finished!')
