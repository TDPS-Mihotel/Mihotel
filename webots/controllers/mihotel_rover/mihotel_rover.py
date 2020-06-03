"""Mihotel rover"""

import multiprocessing
import os
import sys
import time
import psutil
import queue

# flags ########################################################################
# flag_simulation = True  # turn to False to run for real rover
# run simulation rover if webots software is running
flag_simulation = len([p.name() for p in psutil.process_iter() if 'webots' in p.name()])
flag_patio_finished = multiprocessing.Value('i', False)
key = multiprocessing.Value('i', True)
simulation_time = multiprocessing.Value('f', 0.0)

# import depending on simulation or not ########################################
if flag_simulation:
    os.chdir(sys.path[0])
    sys.path.append('../../../')

import chassis
import decision
import detection
from colored import commandInfo, debugInfo, stateInfo, detectedInfo, info, logoInfo, clock


# define the processes #########################################################
def control(command_queue, motors_queue, simulation_time):
    controller = chassis.Controller()
    command = ''
    frame = 0
    while True:
        time.sleep(0.01)
        is_changed = False
        while True:
            controller.set_state(command, simulation_time.value)
            if command_queue.empty():
                break
            else:
                command, frame = command_queue.get()
        while True:
            try:
                motors_queue.get(block=True, timeout=0.005)
            except queue.Empty:
                break
        motors_queue.put((controller.velocityDict, frame))
        # commandInfo('Chassis frame: ' + str(frame))


def detect(signal_queue, key, sensors_queue):
    detector = detection.Detector()
    while True:
        time.sleep(0.01)
        is_changed = False
        # update sensors data
        while not sensors_queue.empty():
            (
                detector.time,
                # detector.gpsRaw_position,
                # detector.gpsRaw_speed,
                detector.compassRaw,
                detector.camerasRaw
            ), frame = sensors_queue.get()
            is_changed = True
        if is_changed:
            start = time.time()
            # detectedInfo('Detector frame: ' + str(frame))
            detector.process()
            # send all signals except object detection to decider
            signal_queue.put((detector.signals, frame))
            detector.object_detection()
            # object detection updated
            signal_queue.put((detector.signals, frame))
        # keyboard events
        # if key.value == ord('C'):  # capture image when C is pressed
        #     detector.capture('path')


def decide(signal_queue, command_queue, simulation_time, key, lock, flag_patio_finished):
    decider = decision.Decider()
    while True:
        time.sleep(0.01)
        # update signals
        is_changed = False
        while not signal_queue.empty():
            decider.signals, frame = signal_queue.get()
            is_changed = True
        if is_changed:
            decider.state_machine()
            command_queue.put((decider.command, frame))
            # stateInfo('Decider frame: ' + str(frame))


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
    detector_process = multiprocessing.Process(target=detect, args=(signal_queue, key, sensors_queue))
    decider_process = multiprocessing.Process(target=decide, args=(
        signal_queue, command_queue, simulation_time, key, lock, flag_patio_finished))
    controller_process = multiprocessing.Process(target=control, args=(command_queue, motors_queue, simulation_time))
    detector_process.daemon = True
    controller_process.daemon = True
    decider_process.daemon = True
    detector_process.start()
    decider_process.start()
    controller_process.start()

# if run for webots rover
if __name__ == "__main__" and flag_simulation:
    from controller import Robot, Keyboard
    # create the Robot instance.
    robot = Robot()
    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep()) * 2
    # enable keyboard listening
    # keyboard = Keyboard()
    # keyboard.enable(timestep)
    # enable sensors
    sensors = detection.Sensors(robot)
    # enable motors
    motors = chassis.WebotsMotorsGroup(robot)

    frame = -1
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while (robot.step(timestep) != -1) and not flag_patio_finished.value:
        frame += 1
        start = time.time()
        simulation_time.value = sensors.getTime()
        is_changed = False
        # debugInfo('Simulation frame: ' + str(frame))
        # update sensors data
        if sensors_queue.empty():
            sensors_queue.put((sensors.update(), frame))
        # update motors speed
        # while not motors_queue.empty():
        try:
            velocityDict, motor_frame = motors_queue.get(block=True, timeout=0.01)
            motors.update(velocityDict)
            # commandInfo('Motor frame: ' + str(motor_frame))
        except queue.Empty:
            pass
        # debugInfo(int((time.time() - start) * 1000))
        # with lock:
        #     key.value = keyboard.getKey()  # character of the key press

# if run for real rover
if __name__ == "__main__" and not flag_simulation:
    # when flag_patio_finished becomes True, main process ends, and all child
    # processes end with it
    key.value = 1000  # it is useless for real rover now
    while not flag_patio_finished.value:
        # temporarily using time to be the finish flag signal
        if time.time() - start > 2:  # 2s
            flag_patio_finished.value = True

if __name__ == "__main__":
    # clean up
    for queue in queueList:
        queue.close()
    info('Finished!')
