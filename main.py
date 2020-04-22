import multiprocessing
import time

import chassis
import decision
import detection
from colored import commandInfo, debugInfo, detectedInfo, info, logoInfo

# flags ########################################################################
flag_patio_finished = 0


# define the processes #########################################################
def control(command_queue):
    controller = chassis.Controller()
    while True:
        if not command_queue.empty():
            controller.set_state(command_queue.get())


def detect(signal_queue):
    detector = detection.Detector()
    detector.run(signal_queue)


def decide(signal_queue, command_queue):
    decider = decision.Decider()
    decider.run(signal_queue, command_queue)


# program starts ###############################################################
if __name__ == "__main__":
    start = time.time()
    logoInfo()

    # create pipes
    command_queue = multiprocessing.Queue()
    signal_queue = multiprocessing.Queue()

    # initial processes and set them as deamon process
    controller_process = multiprocessing.Process(target=control, args=(command_queue, ))
    detector_process = multiprocessing.Process(target=detect, args=(signal_queue, ))
    decider_process = multiprocessing.Process(target=decide, args=(signal_queue, command_queue,))
    controller_process.daemon = True
    detector_process.daemon = True
    decider_process.daemon = True
    controller_process.start()
    detector_process.start()
    decider_process.start()

    # when flag_patio_finished becomes True, program ends, and all processes end with it
    while True:
        # now use time to be finish flag signal
        if time.time() - start > 1:  # 1s
            flag_patio_finished = True
        if flag_patio_finished:
            break
    info('Finished 🍻')
